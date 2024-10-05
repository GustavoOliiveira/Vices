// Função para atualizar a fonte do vídeo
function updateVideoSource(theme) {
    var videoElement = document.getElementById('myVideo');
    if (theme === 'dark') {
        videoElement.src = '/assets/CentralPage/psico-dark.MP4'; // URL do vídeo escuro
    } else {
        videoElement.src = '/assets/CentralPage/psico-light.MP4'; // URL do vídeo claro
    }
    videoElement.load(); // Recarrega o vídeo com a nova fonte
}

// Seleciona o botão e adiciona o evento de clique para abrir/fechar o menu
document.querySelector('.dropdown-btn').addEventListener('click', function() {
    this.parentElement.classList.toggle('show');
});

// Seleciona todas as opções de dropdown
document.querySelectorAll('.dropdown-content a').forEach(option => {
    option.addEventListener('click', function(event) {
        event.preventDefault();  // Evita a navegação do link
        
        // Obtém o valor da opção clicada
        var selectedOption = this.getAttribute('data-theme');

        // Atualiza o texto do botão com a opção selecionada
        document.querySelector('.dropdown-btn').textContent = selectedOption === 'light' ? 'Claro' : 'Escuro';

        // Altera o tema com base na opção selecionada
        if (selectedOption === 'dark') {
            document.body.classList.add('theme-dark'); // Adiciona a classe do tema escuro
            updateVideoSource('dark'); // Atualiza o vídeo para o tema escuro
        } else {
            document.body.classList.remove('theme-dark'); // Remove a classe do tema escuro
            updateVideoSource('light'); // Atualiza o vídeo para o tema claro
        }

        // Fecha o dropdown
        this.parentElement.parentElement.classList.remove('show');
    });
});

// Fecha o dropdown se o usuário clicar fora dele
window.onclick = function(event) {
    if (!event.target.matches('.dropdown-btn')) {
        var dropdowns = document.getElementsByClassName('dropdown-content');
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.parentElement.classList.contains('show')) {
                openDropdown.parentElement.classList.remove('show');
            }
        }
    }
}
