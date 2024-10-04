document.addEventListener("DOMContentLoaded", function() {
    const options = document.querySelectorAll(".option-left-bar");
    const sectionsCenter = document.querySelectorAll(".content-section-center");
    const sectionsRight = document.querySelectorAll(".content-section-bar-right");

    // Função para mostrar a seção correspondente
    function showSection(target) {
        sectionsCenter.forEach(section => section.style.display = "none");
        sectionsRight.forEach(section => section.style.display = "none");

        document.getElementById(target).style.display = "block";
        document.getElementById(`${target}-bar-right`).style.display = "block";
        
        if (target === "ranked") {
            // Exibir a div de boas-vindas ao selecionar "ranked"
            document.getElementById("welcome-overlay").style.display = "flex";
            document.querySelector(".content-mod-section-learn").style.overflow = "hidden";
            document.getElementById("quiz-container").style.display = "block"; // Torna o quiz visível
        }
    }

    options.forEach(option => {
        option.addEventListener("click", function() {
            const target = this.getAttribute("data-option");
            showSection(target);
        });
    });

    // Ocultar a div de boas-vindas ao clicar no botão "Sair"
    document.getElementById("exitButton").addEventListener("click", function() {
        document.getElementById("welcome-overlay").style.display = "none";
    });

    // Exibir a seção "learn" por padrão
    showSection("learn");
});

// ----------- função de marcação das data-option
document.addEventListener('DOMContentLoaded', function () {
    const options = document.querySelectorAll('.option-left-bar');

    options.forEach(option => {
        option.addEventListener('click', function () {
            // Remove a classe 'active' de todas as divs
            options.forEach(opt => opt.classList.remove('active'));
            
            // Adiciona a classe 'active' apenas na div clicada
            this.classList.add('active');
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const questions = document.querySelectorAll(".question-container");
    let currentQuestionIndex = 0;

    const nextButton = document.getElementById("nextButton");
    const finishButton = document.getElementById("finishButton");

    // Função para mostrar a questão atual
    function showQuestion(index) {
        questions.forEach((question, i) => {
            question.style.display = i === index ? "block" : "none";
        });
    }

    // Função para selecionar uma opção
    function selectOption(event) {
        const selectedOption = event.target;
        const options = selectedOption.parentNode.querySelectorAll(".option");

        options.forEach(option => option.classList.remove("selected")); // Remove a seleção de todas as opções
        selectedOption.classList.add("selected"); // Adiciona a classe à opção clicada
    }

    // Adiciona evento de clique às opções
    document.querySelectorAll(".option").forEach(option => {
        option.addEventListener("click", selectOption);
    });

    nextButton.addEventListener("click", () => {
        const currentQuestion = questions[currentQuestionIndex];
        const selectedOption = currentQuestion.querySelector(".selected");

        // Validação para verificar se uma opção foi marcada
        if (!selectedOption) {
            alert("Por favor, selecione uma opção antes de continuar.");
            return;
        }

        currentQuestionIndex++;
        if (currentQuestionIndex < questions.length) {
            showQuestion(currentQuestionIndex);
        } else {
            finishQuiz();
        }
    });

    finishButton.addEventListener("click", finishQuiz);

    // Função para finalizar o quiz
    function finishQuiz() {
        alert("Você completou o quiz!");
        document.getElementById("welcome-overlay").style.display = "none"; // Fechar a página de boas-vindas
    }

    // Inicializa o quiz mostrando a primeira pergunta
    showQuestion(currentQuestionIndex);
});
