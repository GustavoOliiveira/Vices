// Abrir a modal
document.getElementById("openLoginModal").addEventListener("click", function() {
    document.getElementById("loginModal").style.display = "block";
    document.body.style.overflow = "hidden"; // Desativa o scroll
});

// Fechar a modal
document.getElementById("closeModal").addEventListener("click", function() {
    document.getElementById("loginModal").style.display = "none";
    document.body.style.overflow = ""; // Reativa o scroll
});

// Função para abrir a modal
document.querySelector('.bt-comece-agora-first-section').addEventListener('click', function() {
    document.getElementById('modal-comece-agora').style.display = 'block';
    document.body.style.overflow = "hidden"; // Desativa o scroll
});

// Função para fechar a modal ao clicar no botão "x"
document.querySelector('.close-btn-new').addEventListener('click', function() {
    document.getElementById('modal-comece-agora').style.display = 'none';
    document.body.style.overflow = ""; // Reativa o scroll
});

let currentStep = 1;
const totalSteps = 10;
const progressBar = document.getElementById('progress-bar');

// Função para atualizar a barra de progresso
function updateProgressBar() {
    const progressPercentage = (currentStep / totalSteps) * 100;
    progressBar.style.width = progressPercentage + '%';
}

// Função para ir para a próxima pergunta
function goToStep(step) {
    document.querySelector('.quiz-step.active').classList.remove('active');
    document.querySelector(`.quiz-step[data-step="${step}"]`).classList.add('active');
    currentStep = step;
    updateProgressBar();
}

// Função para verificar respostas e enviar ao console
function submitQuiz() {
    const responses = {};
    for (let i = 1; i <= totalSteps; i++) {
        const answer = document.querySelector(`input[name="question${i}"]:checked`);
        if (answer) {
            responses[`question${i}`] = answer.value;
        } else {
            responses[`question${i}`] = null;
        }
    }
    console.log('Respostas:', responses);
}

// Adicionando eventos de clique nos botões
document.querySelectorAll('.next-btn').forEach(button => {
    button.addEventListener('click', () => {
        goToStep(currentStep + 1);
    });
});

document.querySelectorAll('.prev-btn').forEach(button => {
    button.addEventListener('click', () => {
        goToStep(currentStep - 1);
    });
});

document.querySelector('.submit-btn').addEventListener('click', submitQuiz);

// Inicializar a barra de progresso e o questionário
updateProgressBar();


document.addEventListener('DOMContentLoaded', function() {
    // Obtenha todos os radio buttons
    const radioButtons = document.querySelectorAll('input[type="radio"]');

    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            // Remover a classe 'active' de todos os labels
            const labels = document.querySelectorAll('label');
            labels.forEach(label => {
                label.classList.remove('active');
            });

            // Adiciona a classe 'active' ao label correspondente
            const parentLabel = this.parentElement;
            if (parentLabel.tagName === 'LABEL') {
                parentLabel.classList.add('active');
            }
        });
    });
});

// animando conteudo do cell -------------------------------
let animConteudoCell = document.querySelector(".blind-chat");
setTimeout(() => {
    animConteudoCell.style.opacity = "0";
}, 2000);
setTimeout(() => {
    animConteudoCell.style.display = "none";
}, 3500);

const messages = document.querySelectorAll('.message');
let currentIndex = 0;

// Inicialmente, esconde todas as mensagens
messages.forEach((message, index) => {
  if (index !== currentIndex) {
    message.style.display = 'none';
  }
});

document.querySelector('.next-button-phone').addEventListener('click', () => {
  if (currentIndex < messages.length - 1) {
    // Mostra a próxima mensagem
    currentIndex++;
    messages[currentIndex].style.display = 'block';

    // Rola para a última mensagem
    document.querySelector('.chat-box').scrollTop = document.querySelector('.chat-box').scrollHeight;
  } else {
    // Desabilita o botão quando não houver mais mensagens
    document.querySelector('.next-button-phone').disabled = true;
    document.querySelector('.next-button-phone').innerText = 'Fim';
  }
});

