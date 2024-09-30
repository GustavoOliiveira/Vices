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
    }

    options.forEach(option => {
        option.addEventListener("click", function() {
            const target = this.getAttribute("data-option");
            showSection(target);
        });
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
