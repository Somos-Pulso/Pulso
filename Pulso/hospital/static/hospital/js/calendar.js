document.addEventListener('DOMContentLoaded', async function () {
  // ==================== CONFIGURAÇÕES INICIAIS ====================
  const periodo_inicio = window.hospital.schedule.startDate;
  const periodo_fim = window.hospital.schedule.endDate;
  const endDatePlusOne = addOneDay(periodo_fim);
  const realStart = new Date(periodo_inicio + 'T12:00:00');
  const realEnd = new Date(periodo_fim + 'T12:00:00');
  
  let originalStartTimes = {};

  // ==================== FUNÇÕES AUXILIARES ====================
  function addOneDay(dateString) {
    const date = new Date(dateString + 'T12:00:00');
    date.setDate(date.getDate() + 1);
    return date.toISOString().split('T')[0];
  }

  function limparHoras(date) {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    return d;
  }

  function formatDateLocal(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

  function formatTime(time) {
    return time?.padStart(5, '0') || '--:--';
  }

  function isDateInPast(date, includeToday = false) {
    const now = new Date();
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (includeToday) {
      return date < today;
    }
    return date < now;
  }

  function isDateInRange(date) {
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    
    const realStartDate = new Date(realStart);
    realStartDate.setHours(0, 0, 0, 0);
    const realEndDate = new Date(realEnd);
    realEndDate.setHours(0, 0, 0, 0);
    
    const oneDay = 24 * 60 * 60 * 1000;
    const realEndDatePlusOne = new Date(realEndDate.getTime() + oneDay);
    
    return date >= hoje && date >= realStartDate && date < realEndDatePlusOne;
  }

  // ==================== PREPARAÇÃO DOS EVENTOS ====================
  const fcEvents = window.hospital.data.shifts.map(ev => ({
    id: String(ev.id),
    title: `${ev.start_time} - ${ev.end_time}`,
    start: `${ev.date}T${ev.start_time}:00`,
    end: `${ev.date}T${ev.end_time}:00`,
    extendedProps: {
      id: ev.id,
      createdBy: ev.created_by,
      startTime: ev.start_time,
      endTime: ev.end_time,
      description: ev.description,
      allocations: ev.allocations
    },
    className: ev.type
  }));

  // ==================== HANDLERS DE EVENTOS ====================
  function handleEventDragStart(info) {
    originalStartTimes[info.event.id] = info.event.start;
  }

  function handleEventDrop(info) {
    const event = info.event;
    const start = new Date(event.start);
    const end = new Date(event.end);
    const originalStart = originalStartTimes[event.id];
    const now = new Date();

    if (originalStart < now) {
      console.warn("Evento já começou, não pode ser movido.");
      info.revert();
      return;
    }
    
    const eventDateStr = event.startStr.split("T")[0];
    const eventStartTime = event.extendedProps.startTime;
    const eventStartDateTime = new Date(`${eventDateStr}T${eventStartTime}:00`);

    if (eventStartDateTime < now) {
      console.warn("Não pode mover para um horário já passado.");
      info.revert();
      return;
    }

    if (!isDateInRange(start) || !isDateInRange(end)) {
      console.warn("Fora do intervalo permitido.");
      info.revert();
      return;
    }

    const novoPlantaoData = formatDateLocal(start);
    const novoInicio = start.toTimeString().slice(0, 5);
    const novoFim = end.toTimeString().slice(0, 5);

    const requestData = {
      schedule_id: window.hospital.schedule.id,
      shift: {
        date: novoPlantaoData,
        start_time: novoInicio,
        end_time: novoFim,
        description: event.extendedProps.description || "",
        allocations: (event.extendedProps.allocations || []).map((medico) => ({
          doctor_id: medico.doctor_id ?? medico.id,
        }))
      },
    };

    const plantaoId = event.extendedProps.id;
    const url = window.hospital.urls.updateShift.replace("<id>", plantaoId);

    fetch(url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": window.getCookie("csrftoken"),
      },
      body: JSON.stringify(requestData),
    })
      .then(async (res) => {
        const data = await res.json();
        if (data.error) {
          info.revert();
          return;
        }
        handleSaveSuccess(data.shift, true, plantaoId);
      })
      .catch((err) => {
        console.error("Erro na requisição:", err);
        info.revert();
      });
  }

  function handleDayCellMount(info) {
    const date = new Date(info.date.getFullYear(), info.date.getMonth(), info.date.getDate(), 12);
    const isOutOfRange = date < realStart || date > realEnd;
    const isOtherMonth = info.isOther;
    const el = info.el;

    if (isOutOfRange && !isOtherMonth) {
      el.style.opacity = '0.3';
    }
    if (isOtherMonth && !isOutOfRange) {
      el.style.opacity = '0.75';
    }
    if (isOtherMonth && isOutOfRange) {
      el.style.opacity = '1';
    }
  }

  function handleEventClick(info) {
    info.jsEvent.preventDefault();
    
    const modal = document.getElementById("modal-detalhe");
    const eventDate = info.event.startStr.split("T")[0];
    const date = new Date(`${eventDate}T12:00:00`);
    
    setupModalData(modal, info, eventDate, date);
    
    setupModalButtons(modal, eventDate, info.event.extendedProps);

    setupEventDetails(modal, info.event.extendedProps, date);
    
    setupAllocatedDoctors(modal, info.event.id);

    positionAndShowModal(modal, info.jsEvent);
  }

  function handleDateClick(info) {
    const clickDate = new Date(info.dateStr + 'T12:00:00');
    const ontem = new Date();
    ontem.setDate(ontem.getDate());
    ontem.setHours(0, 0, 0, 0);

    if (clickDate <= ontem) return;

    if (clickDate >= realStart && clickDate <= realEnd) {
      fechardetalhe();
      criarplantao({
        date: info.dateStr,
        weekday: clickDate.toLocaleDateString('pt-BR', { weekday: 'long' }),
        hour: 0,
      });
    }
  }

  function handleSelect(info) {
    const start = new Date(info.startStr);
    const end = new Date(info.endStr);
    const dateStr = info.startStr.split("T")[0];
    const now = new Date();
    now.setSeconds(0, 0);
    const hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    const realStart = new Date(periodo_inicio + 'T00:00:00');
    realStart.setHours(0, 0, 0, 0);
    const dataSelecionada = new Date(dateStr + 'T00:00:00');

    if (dataSelecionada < hoje) return;
    if (dataSelecionada.getTime() === hoje.getTime() && start < now) return;
    if (start < realStart || end > realEnd) {
      console.warn("Fora do intervalo permitido");
      return;
    }

    fechardetalhe();
    criarplantao({
      date: dateStr,
      weekday: start.toLocaleDateString("pt-BR", { weekday: "long" }),
      hour: start.getHours()
    });
  }

  // ==================== FUNÇÕES DE CONFIGURAÇÃO DO MODAL ====================
  function setupModalData(modal, info, eventDate, date) {
    modal.dataset.plantaoId = info.event.extendedProps.id;
    modal.dataset.currentDate = eventDate;
    modal.dataset.currentStart = info.event.extendedProps.startTime;
    modal.dataset.currentEnd = info.event.extendedProps.endTime;
    modal.dataset.currentDescription = info.event.extendedProps.description || "";
    modal.dataset.currentWeekday = date.toLocaleDateString("pt-BR", { weekday: "long" });
    modal.dataset.createdBy = info.event.extendedProps.createdBy;
  }

  function setupModalButtons(modal, eventDate, extendedProps) {
    const btnEditar = modal.querySelector("#shift-edit-button");
    const btnExcluir = modal.querySelector("#shift-delete-button");
    const url = window.hospital.urls.viewShift.replace("<id>", extendedProps.id);
    const detailBtn = modal.querySelector(".icon-detail");
    
    detailBtn.dataset.url = url;
    modal.querySelector('.icon-detail').dataset.url = url;

    const fullDateTime = new Date(`${eventDate}T${extendedProps.startTime}`);
    const now = new Date();
    const isPast = fullDateTime < now;

    [btnEditar, btnExcluir].forEach((btn) => {
      if (!btn) return;
      if (isPast) {
        btn.disabled = true;
        btn.classList.add("disabled");
        btn.title = "Plantão já ocorreu";
      } else {
        btn.disabled = false;
        btn.classList.remove("disabled");
        btn.title = btn.classList.contains("icon-edit") ? "Editar" : "Excluir";
      }
    });
  }

  function setupEventDetails(modal, extendedProps, date) {
    document.getElementById("detalhe-data").textContent = date.toLocaleDateString("pt-BR", {
      weekday: "long",
      day: "2-digit",
      month: "2-digit",
      year: "numeric"
    });
    document.getElementById("detalhe-start").textContent = extendedProps.startTime;
    document.getElementById("detalhe-end").textContent = extendedProps.endTime;
    document.getElementById("detalhe-description").textContent = 
      (extendedProps.description || "").trim() || "Sem descrição";
  }

  function setupAllocatedDoctors(modal, eventId) {
    const ul = document.getElementById("detalhe-medicos");
    ul.innerHTML = "";
    
    const plantaoAtualizado = window.hospital.data.shifts.find(p => p.id == eventId);
    const allocations = plantaoAtualizado ? plantaoAtualizado.allocations || [] : [];
    modal.dataset.currentAllocations = JSON.stringify(allocations);

    ul.classList.add("avatar-stack");

    if (allocations.length === 0) {
      ul.innerHTML = `<li class="text-muted">Nenhum médico alocado.</li>`;
    } else {
      allocations.forEach((aloc, i) => {
        const li = document.createElement("li");
        li.className = "d-inline-block";
        li.style.marginLeft = i > 0 ? "-12px" : "0";

        const img = document.createElement("img");
        img.src = aloc.photo || window.hospital.static.defaultPhoto;
        img.alt = `Médico ${aloc.id}`;
        img.title = `Nome: ${aloc.username} | Status: ${aloc.status}`;
        img.className = "avatar-img";

        
        if (aloc.is_conflicted) {
          img.classList.add("conflicted-allocation");
        } else {
          switch (aloc.status) {
            case "Confirmada":
              console.warn(aloc.status)
              img.classList.add("confirmed-allocation");
              break;
            case "Recusada":
              console.warn(aloc.status)
              img.classList.add("rejected-allocation");
              break;
            case "Em Aberto":
              console.warn(aloc.status)
              img.classList.add("pending-allocation");
              break;
          }
        }

        li.appendChild(img);
        ul.appendChild(li);
      });
      }
    }

  function positionAndShowModal(modal, jsEvent) {
    const container = document.getElementById('calendar-container');
    const containerRect = container.getBoundingClientRect();

    modal.style.visibility = "hidden";
    modal.style.display = "block";

    const modalWidth = modal.offsetWidth;
    const modalHeight = modal.offsetHeight;
    const PADDING = 10;
    const containerWidth = container.offsetWidth;
    const containerHeight = container.offsetHeight;

    let x = jsEvent.pageX - (containerRect.left + window.scrollX);
    let y = jsEvent.pageY - (containerRect.top + window.scrollY);

    if ((x + modalWidth + PADDING) > containerWidth) {
      x = containerWidth - modalWidth - PADDING;
    }
    if (x < PADDING) {
      x = PADDING;
    }
    if ((y + modalHeight + PADDING) > containerHeight) {
      y = containerHeight - modalHeight - PADDING;
    }
    if (y < PADDING) {
      y = PADDING;
    }

    modal.style.left = `${x - 10}px`;
    modal.style.top = `${y - 10}px`;
    modal.style.position = "absolute";
    modal.style.zIndex = 2000;
    modal.classList.remove("hidden");
    modal.style.opacity = "1";
    modal.style.display = "block";
    modal.style.visibility = "visible";
  }

  function handleEventContent(arg) {
    const startTime = arg.event.extendedProps.startTime || '';
    const endTime = arg.event.extendedProps.endTime || '';
    const formattedStart = formatTime(startTime);
    const formattedEnd = formatTime(endTime);
    const classes = Array.isArray(arg.event.classNames)
      ? arg.event.classNames.join(' ')
      : (arg.event.classNames || '');

    const allocations = arg.event.extendedProps.allocations || [];


    const hasRejected = allocations.some(a => a.status === "Recusada");
    const hasConflict = allocations.some(a => a.is_conflicted === true);

    let alertsHTML = "";
    if (arg.event.classNames != "past-shift"){
      if (hasRejected) {
        alertsHTML += `
          <span title="Médico recusou" class="icon-alert rejected-alert">
            <img src="${window.hospital.static.rejectedIcon}" alt="Recusado" />
          </span>
        `;
      }

      if (hasConflict) {
        alertsHTML += `
          <span title="Médico em conflito" class="icon-alert conflicted-alert">
            <img src="${window.hospital.static.conflictedIcon}" alt="Conflito"/>
          </span>
        `;
      }
    }

    return {
      html: `
        <div class="custom-event ${classes}">
          <div class="event-time">${formattedStart} - ${formattedEnd}</div>
          <div class="event-alerts">${alertsHTML}</div>
        </div>
      `
    };
  }
  // ==================== CONFIGURAÇÃO DO CALENDÁRIO ====================
  const calendarEl = document.getElementById('calendar');
  window.calendar = new FullCalendar.Calendar(calendarEl, {
    locale: 'pt-br',
    timeZone: 'local',
    initialView: 'dayGridMonth',
    initialDate: new Date(periodo_inicio + 'T12:00:00'),
    headerToolbar: false,
    showNonCurrentDates: true,
    fixedWeekCount: false,
    allDaySlot: false,
    height: 'auto',
    contentHeight: 'auto',
    dayMaxEvents: 3,
    selectable: true,
    editable: true,
    
    // Event Handlers
    eventDragStart: handleEventDragStart,
    eventDrop: handleEventDrop,
    dayCellDidMount: handleDayCellMount,
    eventClick: handleEventClick,
    dateClick: handleDateClick,
    select: handleSelect,
    eventContent: handleEventContent,

    eventTimeFormat: {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    },

    views: {
      dayGridMonth: {
        showNonCurrentDates: true,
        fixedWeekCount: false
      },
      timeGridDay: {
        slotMinTime: '00:00:00',
        slotMaxTime: '24:00:00',
        allDaySlot: false
      },
      timeGridWeek: {
        slotMinTime: '00:00:00',
        slotMaxTime: '24:00:00',
        allDaySlot: false
      }
    },

    events: fcEvents
  });

  calendar.render();

  // ==================== NAVEGAÇÃO DO CALENDÁRIO ====================
  function updateDate() {
    const current = calendar.getDate();
    const label = current.toLocaleDateString('pt-BR', {
      year: 'numeric',
      month: 'long',
    });
    document.getElementById('current-month').innerText =
      label.charAt(0).toUpperCase() + label.slice(1);
  }

  function getDeltaDays(viewType) {
    if (viewType.includes('Month')) return 30;
    if (viewType.includes('Week')) return 7;
    if (viewType.includes('Day')) return 1;
    return 7;
  }

  function isDateAllowed(targetDate) {
    const start = new Date(realStart.getFullYear(), realStart.getMonth(), 1);
    const end = new Date(realEnd.getFullYear(), realEnd.getMonth() + 1, 0);
    return targetDate >= start && targetDate <= end;
  }

  function navigateCalendar(direction) {
    const current = calendar.getDate();
    const viewType = calendar.view.type;
    const delta = getDeltaDays(viewType);

    const target = new Date(current);
    target.setDate(target.getDate() + (direction === 'next' ? delta : -delta));

    if (isDateAllowed(target)) {
      calendar[direction]();
      updateDate();
    }
  }

  // ==================== EVENT LISTENERS ====================
  updateDate();

  document.getElementById('prev').addEventListener('click', () => navigateCalendar('prev'));
  document.getElementById('next').addEventListener('click', () => navigateCalendar('next'));

  document.querySelectorAll('.calendar-nav .nav-link').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const view = this.dataset.view;
      calendar.changeView(view);
      updateDate();
      document.querySelectorAll('.calendar-nav .nav-link').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
    });
  });

  document.getElementById('clear-all').addEventListener('click', function () {
    if (confirm("Tem certeza que quer apagar todos os eventos? Essa ação é irreversível.")) {
      calendar.getEvents().forEach(event => event.remove());
    }
  });
});