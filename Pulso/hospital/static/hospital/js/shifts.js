// ============================================================================
// CONFIGURAÇÃO E INICIALIZAÇÃO
// ============================================================================

function initializeEventListeners() {
  // Event listeners para modais
  document.addEventListener("click", handleModalClicks)
  document.addEventListener("keydown", handleKeyboardEvents)

  // Event listener para checkboxes de médicos
  document.addEventListener("change", handleDoctorCheckboxChange)
}

function handleModalClicks(e) {
  const modalDetalhe = document.getElementById("modal-detalhe")
  const modalEdicao = document.getElementById("modal-edicao")

  if (e.target === modalDetalhe) {
    fechardetalhe()
  }
  if (e.target === modalEdicao) {
    fecharmodal()
  }
}

function handleKeyboardEvents(e) {
  if (e.key === "Escape") {
    fechardetalhe()
    fecharmodal()
  }
}

function handleDoctorCheckboxChange(event) {
  if (event.target.classList.contains("medico-checkbox")) {
    const id = Number.parseInt(event.target.id.replace("chk", ""))

    if (event.target.checked) {
      window.hospital.data.allocatedDoctors.add(id)
    } else {
      window.hospital.data.allocatedDoctors.delete(id)
    }

    window.atualizarMedicosAlocados()
  }
}

// ============================================================================
// UTILITÁRIOS DE DATA/HORA - CORRIGIDOS PARA FUSO HORÁRIO LOCAL
// ============================================================================

/**
 * Cria uma data local sem conversão de fuso horário
 */
function createLocalDate(year, month, day, hour = 0, minute = 0, second = 0) {
  return new Date(year, month, day, hour, minute, second)
}

/**
 * Converte string de data (YYYY-MM-DD) para Date local
 */
function parseLocalDate(dateString) {
  const [year, month, day] = dateString.split("-").map(Number)
  return createLocalDate(year, month - 1, day)
}

/**
 * Converte Date para string no formato YYYY-MM-DD (local)
 */
function formatLocalDate(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, "0")
  const day = String(date.getDate()).padStart(2, "0")
  return `${year}-${month}-${day}`
}

/**
 * Converte string de horário (HH:MM) para Date local na data especificada
 */
function parseLocalDateTime(dateString, timeString) {
  const [year, month, day] = dateString.split("-").map(Number)
  const [hour, minute] = timeString.split(":").map(Number)
  return createLocalDate(year, month - 1, day, hour, minute)
}

/**
 * Formata Date para string de horário (HH:MM)
 */
function formatLocalTime(date) {
  const hour = String(date.getHours()).padStart(2, "0")
  const minute = String(date.getMinutes()).padStart(2, "0")
  return `${hour}:${minute}`
}

/**
 * Valida se um horário está no futuro (considerando data e hora)
 */
function isTimeInFuture(dateString, timeString) {
  const targetDateTime = parseLocalDateTime(dateString, timeString)
  const now = new Date()

  console.log("Validando horário:", {
    target: targetDateTime,
    now: now,
    isFuture: targetDateTime > now,
  })

  return targetDateTime > now
}

/**
 * Valida se um horário de fim é posterior ao de início
 */
function isEndTimeAfterStart(dateString, startTime, endTime) {
  const startDateTime = parseLocalDateTime(dateString, startTime)
  const endDateTime = parseLocalDateTime(dateString, endTime)

  // Se o horário de fim for menor, assume que é no dia seguinte
  if (endDateTime <= startDateTime) {
    endDateTime.setDate(endDateTime.getDate() + 1)
  }

  return endDateTime > startDateTime
}

// ============================================================================
// GERENCIAMENTO DE PLANTÕES - CRIAÇÃO E EDIÇÃO
// ============================================================================

const criarplantao = (eventData) => {
  const modal = document.getElementById("modal-edicao")
  if (!modal) {
    console.error("Modal de edição não encontrado")
    return
  }

  clearModalState()

  if (isEditingMode(eventData)) {
    setupEditingMode(eventData, modal)
  } else {
    setupCreationMode(eventData, modal)
  }

  window.atualizarMedicosAlocados()
  modal.classList.remove("hidden")
}

function isEditingMode(eventData) {
  return eventData.start && eventData.extendedProps
}

function clearModalState() {
  const descInput = document.getElementById("edicao-descricao")
  descInput.value = ""

  if (!window.hospital.data.allocatedDoctors) {
    window.hospital.data.allocatedDoctors = new Set()
  } else {
    window.hospital.data.allocatedDoctors.clear()
  }

  document.querySelectorAll(".medico-checkbox").forEach((checkbox) => {
    checkbox.checked = false
  })
}

function setupEditingMode(eventData, modal) {
  document.getElementById("bnt-delete-shift").style.display = "block"

  const { spanData, startInput, endInput, descInput, createdBy, department } = getModalElements()

  createdBy.textContent = window.hospital.schedule.createdBy
  department.textContent = window.hospital.schedule.department

  const { startDate, endDate, weekday, formatted } = processEventDates(eventData)
  spanData.textContent = `${weekday}, ${formatted}`

  const timeData = formatEventTimes(startDate, endDate)
  startInput.value = timeData.startTime
  endInput.value = timeData.endTime

  descInput.value = eventData.extendedProps.description || ""

  setupAllocatedDoctors(eventData.extendedProps.allocations || [])

  setModalData(modal, startDate, weekday, true, eventData.extendedProps.id)
}

function setupCreationMode(eventData, modal) {
  document.getElementById("bnt-delete-shift").style.display = "none"

  const { spanData, startInput, endInput, createdBy, department } = getModalElements()

  createdBy.textContent = window.hospital.schedule.createdBy
  department.textContent = window.hospital.schedule.department

  const { dateObj, formatted } = processCreationDate(eventData.date)
  spanData.textContent = `${eventData.weekday}, ${formatted}`

  const { startTime, endTime } = getDefaultTimes(eventData.hour)
  startInput.value = startTime
  endInput.value = endTime

  setModalData(modal, eventData.date, eventData.weekday, false, "")
}

function getModalElements() {
  return {
    spanData: document.getElementById("edicao-data"),
    startInput: document.getElementById("edicao-start"),
    endInput: document.getElementById("edicao-end"),
    descInput: document.getElementById("edicao-descricao"),
    createdBy: document.getElementById("edicao-manager"),
    department: document.getElementById("edicao-department"),
  }
}

function processEventDates(eventData) {
  // Processar datas mantendo o fuso horário local
  const startDate = eventData.start instanceof Date ? eventData.start : new Date(eventData.start)
  const endDate = eventData.end instanceof Date ? eventData.end : new Date(eventData.end)

  // Criar data local para exibição
  const dateObj = createLocalDate(startDate.getFullYear(), startDate.getMonth(), startDate.getDate(), 12, 0, 0)

  const formatted = dateObj.toLocaleDateString("pt-BR")
  const weekdayNames = [
    "Domingo",
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
  ]
  const weekday = weekdayNames[dateObj.getDay()]

  return { startDate, endDate, weekday, formatted }
}

function formatEventTimes(startDate, endDate) {
  return {
    startTime: formatLocalTime(startDate),
    endTime: formatLocalTime(endDate),
  }
}

function setupAllocatedDoctors(allocations) {
  console.log("Configurando médicos alocados:", allocations)

  window.hospital.data.allocatedDoctors.clear()

  const allocationIds = new Set()

  allocations.forEach((allocation) => {
    const doctorId = allocation.doctor_id || allocation.id || allocation
    if (doctorId) {
      const id = Number.parseInt(doctorId)
      allocationIds.add(id)
      window.hospital.data.allocatedDoctors.add(id)
      console.log(`✓ Médico adicionado ao Set: ID ${id}`)
    }
  })

  document.querySelectorAll(".medico-checkbox").forEach((checkbox) => {
    const checkboxId = Number.parseInt(checkbox.id.replace("chk", ""))
    const isAllocated = window.hospital.data.allocatedDoctors.has(checkboxId)
    checkbox.checked = isAllocated

    if (isAllocated) {
      console.log(`✓ Checkbox marcado: ID ${checkboxId}`)
    }
  })

  console.log("Médicos alocados final:", Array.from(window.hospital.data.allocatedDoctors))
}

function processCreationDate(dateString) {
  const dateObj = parseLocalDate(dateString)
  const formatted = dateObj.toLocaleDateString("pt-BR")
  return { dateObj, formatted }
}

function getDefaultTimes(hour) {
  const startHour = String(hour ?? 0).padStart(2, "0")
  const endHour = String((Number.parseInt(startHour) + 1) % 24).padStart(2, "0")

  return {
    startTime: `${startHour}:00`,
    endTime: `${endHour}:00`,
  }
}

function setModalData(modal, date, weekday, isEditing, plantaoId) {
  modal.dataset.currentDate = typeof date === "string" ? date : formatLocalDate(date)
  modal.dataset.currentWeekday = weekday
  modal.dataset.isEditing = isEditing.toString()
  modal.dataset.plantaoId = plantaoId
}

// ============================================================================
// GERENCIAMENTO DE MÉDICOS ALOCADOS
// ============================================================================

window.atualizarMedicosAlocados = () => {
  const container = document.getElementById("medicos-alocados")
  const alocados = window.hospital.data.doctors.filter((doc) => window.hospital.data.allocatedDoctors.has(doc.id))

  if (alocados.length === 0) {
    container.innerHTML = `<p class="text-muted">Nenhum médico alocado ainda.</p>`
    return
  }

  const html = `
    <ul class="list-unstyled">
      ${alocados
        .map(
          (doc) => `
        <li class="medico-alocado d-flex align-items-center mb-2" title="${doc.nome}">
          <img src="${doc.foto_url || window.hospital.static.defaultPhoto}" 
               alt="${doc.nome}" 
               class="medico-foto-alocado rounded-circle me-2" 
               style="width:40px; height:40px; object-fit: cover;">
        </li>
      `,
        )
        .join("")}
    </ul>
  `

  container.innerHTML = html
}

// ============================================================================
// EDIÇÃO DE PLANTÕES EXISTENTES
// ============================================================================

const editarPlantao = () => {
  const modalDetalhe = document.getElementById("modal-detalhe")

  if (!modalDetalhe.dataset.currentDate || !modalDetalhe.dataset.currentStart) {
    console.warn("Modal sem dados de plantão.")
    return
  }

  const currentEvent = findCurrentEvent(modalDetalhe.dataset.plantaoId)

  if (currentEvent) {
    handleEventFound(currentEvent)
  } else {
    handleEventNotFound(modalDetalhe)
  }
}

function findCurrentEvent(plantaoId) {
  const currentEvents = window.calendar.getEvents()
  return currentEvents.find((event) => {
    return String(event.extendedProps.id) === plantaoId
  })
}

function handleEventFound(currentEvent) {
  console.log("Evento encontrado para edição:", currentEvent)

  const allocations = currentEvent.extendedProps.allocations || []
  console.log("Alocações encontradas:", allocations)

  const eventData = {
    start: currentEvent.startStr,
    end: currentEvent.endStr,
    extendedProps: {
      id: currentEvent.extendedProps.id,
      description: currentEvent.extendedProps.description || "",
      allocations: allocations,
    },
  }

  fechardetalhe()
  criarplantao(eventData)
}

function updateCheckboxes() {
  document.querySelectorAll(".medico-checkbox").forEach((cb) => {
    const doctorId = Number.parseInt(cb.id.replace("chk", ""))
    cb.checked = window.hospital.data.allocatedDoctors.has(doctorId)
  })
}

function handleEventNotFound(modalDetalhe) {
  const data = {
    date: modalDetalhe.dataset.currentDate,
    weekday: modalDetalhe.dataset.currentWeekday,
    start: modalDetalhe.dataset.currentStart,
    end: modalDetalhe.dataset.currentEnd,
  }

  fechardetalhe()
  setupFallbackModal(data, modalDetalhe.dataset.plantaoId)
}

function setupFallbackModal(data, plantaoId) {
  const modalEdicao = document.getElementById("modal-edicao")
  if (!modalEdicao) {
    console.error("Modal de edição não encontrado")
    return
  }

  const spanData = document.getElementById("edicao-data")
  if (spanData) {
    const { formatted } = processCreationDate(data.date)
    spanData.textContent = `${data.weekday}, ${formatted}`
  }

  document.getElementById("edicao-start").value = data.start
  document.getElementById("edicao-end").value = data.end

  setModalData(modalEdicao, data.date, data.weekday, true, plantaoId || "")
  modalEdicao.classList.remove("hidden")
}

// ============================================================================
// SALVAMENTO DE PLANTÕES - COM VALIDAÇÃO DE FUSO HORÁRIO CORRIGIDA
// ============================================================================

const salvarPlantao = () => {
  const modal = document.getElementById("modal-edicao")
  const isEditing = modal.dataset.isEditing === "true"
  const plantaoId = modal.dataset.plantaoId

  console.log("Salvando plantão:", isEditing ? "EDIÇÃO" : "CRIAÇÃO")
  console.log("ID do plantão:", plantaoId)

  const formData = collectFormData(modal)

  if (!validateFormData(formData, isEditing)) {
    return
  }

  const requestData = buildRequestData(formData)
  const { url, method } = getRequestConfig(isEditing, plantaoId)

  sendSaveRequest(url, method, requestData, isEditing, plantaoId)
}

function collectFormData(modal) {
  const formData = {
    data: modal.dataset.currentDate,
    weekday: modal.dataset.currentWeekday,
    inicio: document.getElementById("edicao-start").value,
    fim: document.getElementById("edicao-end").value,
    descricao: document.getElementById("edicao-descricao").value,
    medicos: [],
  }

  document.querySelectorAll(".medico-checkbox:checked").forEach((checkbox) => {
    const medicoCard = checkbox.closest(".medico-card")
    const nome = medicoCard.querySelector(".medico-nome").textContent
    const especialidade = medicoCard.querySelector(".medico-especialidade").textContent
    const doctorId = checkbox.id.replace("chk", "")

    formData.medicos.push({
      doctor_id: Number.parseInt(doctorId),
      nome: nome.trim(),
      especialidade: especialidade.trim(),
    })
  })

  return formData
}

function validateFormData(formData, isEditing) {
  // Validação básica de campos obrigatórios
  if (!formData.inicio || !formData.fim) {
    alert("Por favor, preencha os horários de início e fim.")
    return false
  }

  // Validação de horário de fim posterior ao início
  if (!isEndTimeAfterStart(formData.data, formData.inicio, formData.fim)) {
    alert("O horário de fim deve ser posterior ao horário de início.")
    return false
  }

  // Para novos plantões, validar se não está no passado
  if (!isEditing) {
    if (!isTimeInFuture(formData.data, formData.inicio)) {
      const targetDate = parseLocalDate(formData.data)
      const today = new Date()

      // Se for hoje, verificar horário. Se for data futura, permitir
      if (formatLocalDate(targetDate) === formatLocalDate(today)) {
        alert("Não é possível criar um plantão com horário no passado.")
        return false
      }
    }
  }

  return true
}

function buildRequestData(formData) {
  return {
    schedule_id: window.hospital.schedule.id,
    shift: {
      date: formData.data,
      start_time: formData.inicio,
      end_time: formData.fim,
      description: formData.descricao || "",
      allocations: formData.medicos.map((medico) => ({
        doctor_id: medico.doctor_id,
      })),
    },
  }
}

function getRequestConfig(isEditing, plantaoId) {
  const url = isEditing ? window.hospital.urls.updateShift.replace("<id>", plantaoId) : window.hospital.urls.createShift
  const method = isEditing ? "PUT" : "POST"

  console.log("URL:", url)
  console.log("Método:", method)

  return { url, method }
}

function sendSaveRequest(url, method, requestData, isEditing, plantaoId) {
  fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": window.getCookie("csrftoken"),
    },
    body: JSON.stringify(requestData),
  })
    .then(async (res) => {
      const data = await res.json()

      if (data.error) {
        alert(`Erro ao ${isEditing ? "atualizar" : "salvar"} plantão: ` + data.error)
        return
      }

      handleSaveSuccess(data.shift, isEditing, plantaoId)
    })
    .catch((error) => {
      console.error("Erro na requisição:", error)
      alert(`Erro ao ${isEditing ? "atualizar" : "salvar"} plantão. Tente novamente.`)
    })
}

function handleSaveSuccess(plantao, isEditing, plantaoId) {
  if (isEditing) {
    updateExistingShift(plantao, plantaoId)
  } else {
    addNewShift(plantao)
  }

  addEventToCalendar(plantao)
  console.log("Novas alocações:", plantao.allocations)

  fecharmodal()
  atualizarResumoDoCalendario()

  const mensagem = isEditing ? "Plantão atualizado com sucesso!" : "Plantão criado com sucesso!"
  console.log(mensagem)
}

function updateExistingShift(plantao, plantaoId) {
  const existingEvent = window.calendar.getEventById(String(plantaoId))
  if (existingEvent) {
    existingEvent.remove()
    window.calendar.refetchEvents()
  }

  const index = window.hospital.data.shifts.findIndex((p) => p.id == plantaoId)
  if (index !== -1) {
    window.hospital.data.shifts[index] = plantao
  }
}

function addNewShift(plantao) {
  window.hospital.data.shifts.push(plantao)
}

function addEventToCalendar(plantao) {
  // Criar datas locais para o calendário
  const startDateTime = parseLocalDateTime(plantao.date, plantao.start_time)
  const endDateTime = parseLocalDateTime(plantao.date, plantao.end_time)

  // Se o horário de fim for menor que o de início, assumir dia seguinte
  if (endDateTime <= startDateTime) {
    endDateTime.setDate(endDateTime.getDate() + 1)
  }

  window.calendar.addEvent({
    id: String(plantao.id),
    title: `${plantao.start_time} - ${plantao.end_time}`,
    start: startDateTime,
    end: endDateTime,
    extendedProps: {
      id: plantao.id,
      startTime: plantao.start_time,
      endTime: plantao.end_time,
      description: plantao.description,
      allocations: plantao.allocations || [],
    },
    className: plantao.type,
  })
}

// ============================================================================
// EXCLUSÃO DE PLANTÕES
// ============================================================================

const deletarPlantao = async () => {
  const modal = document.getElementById("modal-detalhe")
  const plantaoId = modal.dataset.plantaoId

  if (!plantaoId) {
    console.error("ID do plantão não informado.")
    return
  }

  try {
    const response = await fetch(window.hospital.urls.deleteShift.replace("<id>", plantaoId), {
      method: "DELETE",
      headers: {
        "X-CSRFToken": window.getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
    })

    if (response.ok) {
      handleDeleteSuccess(plantaoId)
    } else {
      const err = await response.text()
      console.error("Erro ao deletar:", err)
    }
  } catch (err) {
    console.error("Erro inesperado:", err)
    alert(`Erro inesperado ao tentar deletar o plantão. ${err}`)
  }
}

function handleDeleteSuccess(plantaoId) {
  fechardetalhe()
  fecharmodal()
  removerPlantaoDoCalendario(plantaoId)
  atualizarResumoDoCalendario()
}

const removerPlantaoDoCalendario = (plantaoId) => {
  const event = window.calendar.getEventById(String(plantaoId))
  if (event) {
    event.remove()
  }
}

// ============================================================================
// CONTROLE DE MODAIS
// ============================================================================

const fechardetalhe = () => {
  const modal = document.getElementById("modal-detalhe")
  if (modal) {
    modal.classList.add("hidden")
    modal.classList.remove("visible")
    modal.style.display = "none"
    modal.style.top = null
    modal.style.left = null
  }
}

const fecharmodal = () => {
  const modal = document.getElementById("modal-edicao")
  if (modal) {
    modal.classList.add("hidden")
  }
}

// ============================================================================
// RESUMO E ESTATÍSTICAS
// ============================================================================

function atualizarResumoDoCalendario() {
  const events = window.calendar.getEvents()
  const medicoIds = new Set()
  let plantoesComWarning = 0

  events.forEach((event) => {
    const classList = event.classNames || []
    const alocacoes = event.extendedProps.allocations || []

    if (classList.some((c) => c.includes("unfilled-shift"))) {
      plantoesComWarning++
    }
    alocacoes.forEach((aloc) => {
      if (aloc.id) medicoIds.add(aloc.id)
    })
  })
  updateSummaryDisplay(medicoIds.size, plantoesComWarning)
}

function updateSummaryDisplay(numMedicos, plantoesComWarning) {
  console.warn("Total de plantões vazios:", plantoesComWarning)
  const spanMedicos = document.getElementById("span-num-medicos")
  if (spanMedicos) {
    spanMedicos.textContent = `${String(numMedicos).padStart(2, "0")} Médicos`
  }

  const spanPlantaoWarning = document.getElementById("span-num-plantao-warning")
  if (spanPlantaoWarning) {
    if (plantoesComWarning > 0) {
      spanPlantaoWarning.textContent = `${String(plantoesComWarning).padStart(2, "0")} Plantões`
      spanPlantaoWarning.previousElementSibling.classList.add("vazios")
      spanPlantaoWarning.previousElementSibling.classList.remove("completo")
    } else {
      spanPlantaoWarning.textContent = `Nenhum plantão vazio`
      spanPlantaoWarning.previousElementSibling.classList.add("completo")
      spanPlantaoWarning.previousElementSibling.classList.remove("vazios")
    }
  }
}

// ============================================================================
// UTILITÁRIOS
// ============================================================================

function atualizarContador(textarea) {
  const contador = document.getElementById("contador-desc")
  const atual = textarea.value.length
  const max = textarea.getAttribute("maxlength")
  contador.textContent = `${atual}/${max}`
}

// ============================================================================
// EXPORTAÇÃO
// ============================================================================
window.fechardetalhe = fechardetalhe

// ============================================================================
// INICIALIZAÇÃO
// ============================================================================

// Inicializar event listeners quando o DOM estiver carregado
document.addEventListener("DOMContentLoaded", initializeEventListeners)
