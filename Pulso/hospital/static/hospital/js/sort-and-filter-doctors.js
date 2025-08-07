// ============================================================================
// GERENCIADOR DE MÉDICOS - BUSCA, FILTROS E ORDENAÇÃO
// ============================================================================

// ============================================================================
// UTILITÁRIOS PARA CONVERSÃO DE TEMPO
// ============================================================================

/**
 * Converte formato "HH:MM" para minutos totais
 * @param {string} timeString - String no formato "HH:MM" (ex: "08:30")
 * @returns {number} - Minutos totais
 */
function timeStringToMinutes(timeString) {
  if (!timeString || typeof timeString !== "string") return 0

  const [hours, minutes] = timeString.split(":").map(Number)
  return (hours || 0) * 60 + (minutes || 0)
}

/**
 * Converte formato "HH:MM" para horas decimais
 * @param {string} timeString - String no formato "HH:MM" (ex: "08:30")
 * @returns {number} - Horas em decimal (ex: 8.5)
 */
function timeStringToHours(timeString) {
  return timeStringToMinutes(timeString) / 60
}

/**
 * Calcula a porcentagem de ocupação do médico
 * @param {string} workhours - Horas trabalhadas no formato "HH:MM"
 * @param {string} workload - Carga horária total no formato "HH:MM"
 * @returns {number} - Porcentagem de ocupação (0-1)
 */
function calculateOccupancyRate(workhours, workload) {
  const workhoursMinutes = timeStringToMinutes(workhours)
  const workloadMinutes = timeStringToMinutes(workload)

  if (workloadMinutes === 0) return 0
  return workhoursMinutes / workloadMinutes
}

// ============================================================================
// CONFIGURAÇÃO E INICIALIZAÇÃO
// ============================================================================

function iniciarBuscaMedicosComJson() {
  const input = document.getElementById("srcbar")
  if (!input || !window.hospital.data.doctors) return

  renderizarListaMedicos(window.hospital.data.doctors)
  setupSearchListener(input)
}

function setupSearchListener(input) {
  input.addEventListener("input", () => {
    const termo = input.value.trim().toLowerCase()

    if (!termo) {
      aplicarFiltrosEOrdenar()
      return
    }

    const filtrados = window.hospital.data.doctors.filter((doc) => {
      const nomeMatch = doc.nome.toLowerCase().includes(termo)
      const especialidadesMatch = doc.especialidades.some((especialidade) =>
        especialidade.toLowerCase().includes(termo),
      )
      return nomeMatch || especialidadesMatch
    })

    renderizarListaMedicos(filtrados)
  })
}

// ============================================================================
// RENDERIZAÇÃO DA LISTA DE MÉDICOS
// ============================================================================

function renderizarListaMedicos(medicos) {
  const lista = document.getElementById("lista-medicos")

  const marcados = getMedicosJaMarcados()

  lista.innerHTML = ""

  if (medicos.length === 0) {
    renderizarListaVazia(lista)
    return
  }

  medicos.forEach((doctor) => {
    const li = criarElementoMedico(doctor)
    lista.appendChild(li)
  })

  window.atualizarMedicosAlocados()
}

function getMedicosJaMarcados() {
  return new Set(
    Array.from(document.querySelectorAll(".medico-checkbox:checked")).map((cb) => cb.id.replace("chk", "")),
  )
}

function renderizarListaVazia(lista) {
  const vazio = document.createElement("li")
  vazio.className = "text-muted"
  vazio.style.padding = "1rem"
  vazio.textContent = "Nenhum médico encontrado."
  lista.appendChild(vazio)
}

function criarElementoMedico(doctor) {
  const li = document.createElement("li")
  li.className = "medico-card d-flex justify-content-between align-items-center p-2 mb-2"

  setDoctorElementData(li, doctor)

  li.innerHTML = buildDoctorHTML(doctor)

  return li
}

function setDoctorElementData(li, doctor) {
  // Agora verifica se tem horas trabalhadas usando a conversão
  const workhoursMinutes = timeStringToMinutes(doctor.workhours)
  const ocupado = workhoursMinutes > 0

  li.dataset.nome = doctor.nome
  li.dataset.especialidade = doctor.especialidades.join(", ")
  li.dataset.workload = doctor.workload
  li.dataset.workhours = doctor.workhours
  li.dataset.ocupado = ocupado
}

function buildDoctorHTML(doctor) {
  const checked = window.hospital.data.allocatedDoctors.has(doctor.id) ? "checked" : ""
  const especialidades = doctor.especialidades.join(", ") || "Sem especialidade"

  return `
    <div class="medico-info d-flex align-items-center">
      <img src="${doctor.foto_url || window.hospital.static.defaultPhoto}" class="medico-foto me-3">
      <div class="medico-texto">
        <p class="medico-nome mb-0">Dr. ${doctor.nome}</p>
        <p class="medico-especialidade mb-0">${especialidades}</p>
      </div>
    </div>
    <input type="checkbox" class="medico-checkbox" id="chk${doctor.id}" ${checked}>
  `
}

// ============================================================================
// SISTEMA DE DROPDOWNS
// ============================================================================

function setupDropdownToggle(btnId, menuId) {
  const btn = document.getElementById(btnId)
  const menu = document.getElementById(menuId)

  if (!btn || !menu) return

  const dropdown = btn.closest(".dropdown-custom")

  setupDropdownClick(btn, menu, dropdown)
  setupDropdownOutsideClick(btn, menu, dropdown)
}

function setupDropdownClick(btn, menu, dropdown) {
  btn.addEventListener("click", (e) => {
    e.stopPropagation()
    const isOpen = menu.classList.contains("open")

    closeAllDropdowns()

    if (!isOpen) {
      menu.classList.add("open")
      dropdown.classList.add("open")
    }
  })
}

function setupDropdownOutsideClick(btn, menu, dropdown) {
  document.addEventListener("click", (e) => {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.remove("open")
      dropdown.classList.remove("open")
    }
  })
}

function closeAllDropdowns() {
  document.querySelectorAll(".dropdown-menu.open").forEach((menu) => menu.classList.remove("open"))
  document.querySelectorAll(".dropdown-custom.open").forEach((dd) => dd.classList.remove("open"))
}

// ============================================================================
// FILTROS E ORDENAÇÃO
// ============================================================================

function aplicarFiltrosEOrdenar() {
  const config = getFilterConfig()
  let dadosFiltrados = window.hospital.data.doctors.slice()

  dadosFiltrados = applySearchFilter(dadosFiltrados, config.termoBusca)
  dadosFiltrados = applyWorkloadFilters(dadosFiltrados, config)

  dadosFiltrados = applySortingWithAllocatedPriority(dadosFiltrados, config.ordenarPor)

  renderizarListaMedicos(dadosFiltrados)
}

function getFilterConfig() {
  return {
    ordenarPor: Array.from(document.querySelectorAll("#menuOrdenar input[type=checkbox]:checked")).map((i) => i.value),
    filtrarLivre: document.getElementById("filtroLivre")?.checked || false,
    filtrarCheia: document.getElementById("filtroCheia")?.checked || false,
    termoBusca: document.getElementById("srcbar")?.value.trim().toLowerCase() || "",
  }
}

function applySearchFilter(dados, termoBusca) {
  if (!termoBusca) return dados

  return dados.filter((doc) => {
    const nomeMatch = doc.nome.toLowerCase().includes(termoBusca)
    const especialidadesMatch = doc.especialidades.some((especialidade) =>
      especialidade.toLowerCase().includes(termoBusca),
    )

    return nomeMatch || especialidadesMatch
  })
}

function applyWorkloadFilters(dados, config) {
  const { filtrarLivre, filtrarCheia } = config

  if (!filtrarLivre && !filtrarCheia) return dados

  return dados.filter((doctor) => {
    const occupancyRate = calculateOccupancyRate(doctor.workhours, doctor.workload)

    if (filtrarLivre && occupancyRate < 0.8) return true
    if (filtrarCheia && occupancyRate >= 1.0) return true
    return false
  })
}

function applySorting(dados, ordenarPor) {
  const resultado = dados.slice()

  if (ordenarPor.length === 0) {
    resultado.sort((a, b) => {
      const aIsAllocated = window.hospital.data.allocatedDoctors.has(a.id)
      const bIsAllocated = window.hospital.data.allocatedDoctors.has(b.id)

      if (aIsAllocated && !bIsAllocated) return -1
      if (!aIsAllocated && bIsAllocated) return 1

      return a.nome.localeCompare(b.nome)
    })
    return resultado
  }

  ordenarPor.forEach((ordem) => {
    switch (ordem) {
      case "alfabetica":
        resultado.sort((a, b) => a.nome.localeCompare(b.nome))
        break
      case "livre":
        resultado.sort((a, b) => {
          const aRate = calculateOccupancyRate(a.workhours, a.workload)
          const bRate = calculateOccupancyRate(b.workhours, b.workload)
          return aRate - bRate
        })
        break
      case "ocupado":
        resultado.sort((a, b) => {
          const aRate = calculateOccupancyRate(a.workhours, a.workload)
          const bRate = calculateOccupancyRate(b.workhours, b.workload)
          return bRate - aRate
        })
        break
    }
  })

  return resultado
}

function applySortingWithAllocatedPriority(dados, ordenarPor) {
  const resultado = dados.slice()

  resultado.sort((a, b) => {
    const aIsAllocated = window.hospital.data.allocatedDoctors.has(a.id)
    const bIsAllocated = window.hospital.data.allocatedDoctors.has(b.id)

    // Prioridade para médicos alocados
    if (aIsAllocated && !bIsAllocated) return -1
    if (!aIsAllocated && bIsAllocated) return 1

    // Aplicar ordenação secundária
    if (ordenarPor.length === 0) {
      return a.nome.localeCompare(b.nome)
    }

    const primeiraOrdem = ordenarPor[0]
    switch (primeiraOrdem) {
      case "alfabetica":
        return a.nome.localeCompare(b.nome)
      case "livre":
        const aRate = calculateOccupancyRate(a.workhours, a.workload)
        const bRate = calculateOccupancyRate(b.workhours, b.workload)
        return aRate - bRate
      case "ocupado":
        const aRateOcupado = calculateOccupancyRate(a.workhours, a.workload)
        const bRateOcupado = calculateOccupancyRate(b.workhours, b.workload)
        return bRateOcupado - aRateOcupado
      default:
        return a.nome.localeCompare(b.nome)
    }
  })

  return resultado
}

// ============================================================================
// INICIALIZAÇÃO E EVENT LISTENERS
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  initializeDropdowns()
  initializeFilterListeners()
  initializeSearchListener()

  aplicarFiltrosEOrdenar()
})

function initializeDropdowns() {
  setupDropdownToggle("btnOrdenar", "menuOrdenar")
  setupDropdownToggle("btnFiltrar", "menuFiltrar")
}

function initializeFilterListeners() {
  const inputs = document.querySelectorAll("#menuOrdenar input[type=checkbox], #menuFiltrar input[type=checkbox]")

  inputs.forEach((input) => input.addEventListener("change", aplicarFiltrosEOrdenar))
}

function initializeSearchListener() {
  const buscaInput = document.getElementById("srcbar")
  if (buscaInput) {
    buscaInput.addEventListener("input", aplicarFiltrosEOrdenar)
  }
}

function atualizarMedicos(novosMedicos) {
  window.doctors = novosMedicos
  aplicarFiltrosEOrdenar()
}

// ============================================================================
// EXPORTAÇÕES (caso necessário)
// ============================================================================

window.iniciarBuscaMedicosComJson = iniciarBuscaMedicosComJson
window.atualizarMedicos = atualizarMedicos
window.aplicarFiltrosEOrdenar = aplicarFiltrosEOrdenar

// Exportar funções utilitárias para uso externo se necessário
window.timeStringToMinutes = timeStringToMinutes
window.timeStringToHours = timeStringToHours
window.calculateOccupancyRate = calculateOccupancyRate
