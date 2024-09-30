let savedDates = []; // Array para armazenar os intervalos de datas salvas
let savedEvents = []; // Array para armazenar os eventos salvos
let calendar; // Variável para armazenar a instância do calendário
let currentEvent = null; // Variável para armazenar o evento que está sendo editado
let initialDate = null; // Armazena a data inicial
let isLoadingSavedEvents = false; // Variável para controlar o carregamento de eventos salvos

// Função para inicializar o FullCalendar
function initCalendar() {
    const calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: ''
        },
        events: savedEvents, // Carrega eventos salvos do Local Storage
        eventClick: function(info) {
            currentEvent = info.event; // Armazena o evento atual
            openEditModal(info.event); // Abre o modal para edição
        },
        dateClick: function(info) {
            if (!isLoadingSavedEvents) { // Verifica se não está carregando eventos
                initialDate = info.date; // Define a data inicial
                addInitialEvent(info.date); // Adiciona uma nova data inicial ao clicar
            }
        }
    });
    calendar.render();
}

// Função para carregar as datas salvas e eventos do Local Storage ao carregar a página
function loadSavedData() {
    isLoadingSavedEvents = true; // Ativa o modo de carregamento para evitar a criação de eventos duplicados

    // Carrega savedDates
    const storedDates = localStorage.getItem('savedDates');
    if (storedDates) {
        savedDates = JSON.parse(storedDates);
        savedDates.forEach(dateRange => {
            const dateParts = dateRange.split(' a ');
            if (dateParts.length === 2) {
                const [start, end] = dateParts.map(date => new Date(date));
                if (!isNaN(start.getTime()) && !isNaN(end.getTime())) {
                    addEventToCalendar(start, end, false); // false para não salvar novamente
                }
            }
        });
        updateSavedDatesText(); // Atualiza o texto de datas salvas
        findMaxScore(); // Atualiza a pontuação máxima
        updateLastInterval(); // Atualiza o último intervalo salvo
    } else {
        document.getElementById("savedDates").textContent = 'Nenhuma data salva.';
    }

    // Carrega savedEvents
    const storedEvents = localStorage.getItem('savedEvents');
    if (storedEvents) {
        savedEvents = JSON.parse(storedEvents);
        savedEvents.forEach(event => {
            calendar.addEvent(event); // Adiciona cada evento salvo ao calendário
        });
    }

    isLoadingSavedEvents = false; // Desativa o modo de carregamento após carregar os eventos
}

// Atualiza o texto das datas salvas
function updateSavedDatesText() {
    document.getElementById("savedDates").textContent = savedDates.length > 0 
        ? `Intervalos salvos: ${savedDates.join(', ')}`
        : 'Nenhuma data salva.';
}

// Adiciona um evento ao calendário
function addEventToCalendar(startDate, endDate, save = true) {
    const event = {
        title: `Datas: ${startDate.toLocaleDateString()} a ${endDate.toLocaleDateString()}`,
        start: startDate,
        end: new Date(endDate.getTime() + 24 * 60 * 60 * 1000), // Corrige o dia a mais
        allDay: true
    };
    calendar.addEvent(event);

    const differenceInDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24)) + 1; // Calcula a diferença de dias

    if (save) {
        savedDates.push(`${differenceInDays}`); // Salva apenas a contagem de dias
        localStorage.setItem('savedDates', JSON.stringify(savedDates)); // Atualiza o Local Storage

        // Salva o evento no savedEvents e no Local Storage
        savedEvents.push(event);
        localStorage.setItem('savedEvents', JSON.stringify(savedEvents));
    }

    updateSavedDatesText(); // Atualiza a exibição das datas salvas
    findMaxScore(); // Chama a função para atualizar a pontuação máxima
    updateLastInterval(); // Atualiza o último intervalo salvo
}

// Função para encontrar a pontuação máxima
function findMaxScore() {
    let maxDays = 0;
    let maxDateRange = '';

    savedDates.forEach(dateRange => {
        const days = parseInt(dateRange.split(' ')[0]);
        if (days > maxDays) {
            maxDays = days;
            maxDateRange = dateRange;
        }
    });

    document.getElementById("maxScore").textContent = maxDays > 0 
        ? ` ${maxDateRange}` 
        : '';
}

// Função para atualizar o último intervalo salvo
function updateLastInterval() {
    document.getElementById("lastInterval").textContent = savedDates.length > 0 
        ? ` ${savedDates[savedDates.length - 1]}`
        : '';
}

// Abre o modal para editar o intervalo de datas
function openEditModal(event) {
    const startDate = new Date(event.start);
    const endDate = new Date(event.end);
    document.getElementById("editDatePicker").flatpickr({
        mode: "range",
        defaultDate: [startDate, endDate], // Preenche o seletor com as datas atuais
        onClose: function(selectedDates) {
            if (selectedDates.length === 2) {
                const newStartDate = selectedDates[0];
                const newEndDate = selectedDates[1];
                event.remove(); // Remove o evento anterior
                addEventToCalendar(newStartDate, newEndDate); // Adiciona o evento atualizado
                document.getElementById("modal").style.display = "none"; // Fecha o modal
            }
        }
    });
    document.getElementById("modal").style.display = "flex"; // Exibe o modal
}

// Limpa todas as datas e eventos salvos
function clearAllData() {
    savedDates = [];
    localStorage.removeItem('savedDates'); // Remove as datas salvas do armazenamento

    savedEvents = [];
    localStorage.removeItem('savedEvents'); // Remove os eventos salvos do armazenamento

    calendar.removeAllEvents();

    updateSavedDatesText();
    findMaxScore();
    updateLastInterval();
}

// Fecha o modal ao clicar no "X"
function closeModal() {
    document.getElementById("modal").style.display = "none"; // Fecha o modal
}

// Adiciona um novo evento de data inicial ao clicar no calendário
function addInitialEvent(date) {
    if (initialDate) {
        const event = {
            title: `Data inicial: ${initialDate.toLocaleDateString()}`,
            start: initialDate,
            end: new Date(initialDate.getTime() + 24 * 60 * 60 * 1000), // Marca apenas a data inicial
            allDay: true
        };
        calendar.addEvent(event);
        savedEvents.push(event); // Salva o evento no array de eventos salvos
        localStorage.setItem('savedEvents', JSON.stringify(savedEvents)); // Atualiza o Local Storage
        initialDate = null; // Reseta a data inicial
    } else {
        initialDate = date; // Armazena a data inicial
    }
}

// Exclui o evento atual
function deleteCurrentEvent() {
    if (currentEvent) {
        currentEvent.remove(); 

        savedEvents = savedEvents.filter(event => {
            return !(event.start === currentEvent.start.toISOString() && 
                     event.end === currentEvent.end.toISOString() && 
                     event.title === currentEvent.title);
        });

        localStorage.setItem('savedEvents', JSON.stringify(savedEvents));

        const days = parseInt(currentEvent.title.split(' ')[1]); 
        savedDates = savedDates.filter(dateRange => !dateRange.includes(days + '')); 
        localStorage.setItem('savedDates', JSON.stringify(savedDates));

        updateSavedDatesText();
        findMaxScore();
        updateLastInterval();

        document.getElementById("modal").style.display = "none";
    }
}

// Inicializa o calendário e carrega os dados salvos
document.addEventListener('DOMContentLoaded', function() {
    initCalendar(); // Inicializa o calendário primeiro
    loadSavedData(); // Depois carrega os dados salvos

    const clearButton = document.getElementById('clearButton');
    if (clearButton) {
        clearButton.addEventListener('click', clearAllData);
    }

    const closeButton = document.querySelector('.close');
    if (closeButton) {
        closeButton.addEventListener('click', closeModal);
    }

    const deleteButton = document.getElementById('deleteButton');
    if (deleteButton) {
        deleteButton.addEventListener('click', deleteCurrentEvent);
    }
});
