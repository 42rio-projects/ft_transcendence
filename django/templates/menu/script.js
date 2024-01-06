$(document).ready(function() {
  $("#loginButton").click(function() {
     var username = $("#usernameInput").val();
     var password = $("#passwordInput").val();

     // Verificar credenciais , essa parada aqui ta provisória, claro
     if (username === "admin" && password === "42") {
        // Redirecionar para a próxima página após o login bem-sucedido
        window.location.href = "menu.html";
     } else {
        // Exibir mensagem de erro
        $("#errorMessage").text("Credenciais inválidas. Tente novamente.");
     }
  });
});


document.addEventListener('DOMContentLoaded', function() {
  const colorOptions = document.querySelectorAll('.color-option');

  colorOptions.forEach(function(colorOption) {
      colorOption.addEventListener('click', function() {
          const selectedColor = colorOption.style.backgroundColor;
          console.log('Cor selecionada:', selectedColor);

          colorOptions.forEach(function(option) {
              option.style.border = 'none';
          });
          colorOption.style.border = '2px solid #000';

          // FALTA ENVIAR PARA O BACKEND ESA BUDEGA
      });
  });
});

function trackTimeOnPage() {
  var startTime = new Date().getTime(); // Tempo inicial

  // Atualiza a cada segundo
  setInterval(function() {
      var currentTime = new Date().getTime();
      var elapsedTimeInSeconds = Math.floor((currentTime - startTime) / 1000);

      // Calcula minutos e segundos
      var minutes = Math.floor(elapsedTimeInSeconds / 60);
      var seconds = elapsedTimeInSeconds % 60;

      // Atualiza o elemento com o tempo decorrido
      document.getElementById('clock').textContent = formatTime(minutes, seconds);
  }, 1000);
}

// Formata o tempo em MM:SS
function formatTime(minutes, seconds) {
  return pad(minutes) + ':' + pad(seconds);
}

// Adiciona um zero à esquerda se for necessário
function pad(number) {
  return (number < 10 ? '0' : '') + number;
}

// Inicia a função quando a página é carregada
window.onload = function () {
  trackTimeOnPage();
};