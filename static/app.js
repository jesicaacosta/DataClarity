

// CODIGO PARA LA BARRA DE PROGRESO

$(document).ready(function() {
    //  se ejecuta una vez que todo el  HTML hcargó,  los elementos HTML estén listos para ser manipulados
  
    $('#file-upload').on('change', function() {
      // selecc el elemento con el ID "file-upload" el input de tipo file
      // evento "change" a este elemento q se dispara cada vez que el usuario selecciona un nuevo archivo
  
      var file = this.files[0];
      // Dentro del evento, "this" se refiere al elemento que desewncadeno el evento (el input de archivo)
      // Accedemos al primer archivo seleccionado desde la propiedad "files", (array que contiene todos los archivos seleccionados)
  
      var formData = new FormData();
      //  FormData objeto está diseñado específicamente para enviar datos de formularios, incluidos archivos, a un servidor utilizando AJAX.
  
      formData.append('file', file);
      // El primer argumento especifica la clave bajo la cual se enviará el archivo al servidor (generalmente "file").
      // El segundo argumento es el objeto de archivo real.
  
      $.ajax({ //ajax es una función de jQuery que permite realizar solicitudes asincrónicas (sin recargar la página) al servidor
        url: '/upload', // URL de endpoint de carga
        type: 'POST', //con POSt envio datos AL servidor 
        data: formData,
        processData: false, // Indica a jQuery que no procese automáticamente los datos antes de enviarlos.
        contentType: false, // evita que jQuery establezca un tipo de contenido predeterminado para la solicitud
        xhr: function() {
          var xhr = new window.XMLHttpRequest();
          xhr.upload.addEventListener("progress", function(event) {
            if (event.lengthComputable) {
              var percentComplete = Math.round((event.loaded * 100) / event.total);
              $('.progress-bar').width(percentComplete + '%').attr('aria-valuenow', percentComplete);
            }
          }, false);
          return xhr;
        },
        success: function(response) {
          // Esta función se ejecuta si la solicitud AJAX se completa con éxito (el archivo se cargó sin errores)
          // Aquí debes manejar la respuesta del servidor (por ejemplo, mostrar un mensaje de éxito)
          $('.progress-bar').width('100%').attr('aria-valuenow', 100);
          // Actualiza la barra de progreso al 100% y establece el atributo aria-valuenow para reflejar la finalización
        },
        error: function(error) {
          // Esta función se ejecuta si la solicitud AJAX encuentra un error
          // Debes manejar el error aquí (por ejemplo, mostrar un mensaje de error al usuario)
          console.error(error);
          // Registra el error en la consola para depuración
        }
      });
    });
  });


document.addEventListener('DOMContentLoaded', () => {
    const body = document.getElementById('app-body');
    const toggleButton = document.getElementById('theme-toggle');
    const brandImage = document.querySelector('.navbar-brand img');
    
    // Función principal para cambiar el tema
    function applyTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark-mode');
            // Cambiar el filtro de la imagen DATACLARITY.png para que se vea bien en fondo oscuro
            if (brandImage) {
                // Aplica un filtro CSS inverso (para logos claros en fondo oscuro)
                brandImage.style.filter = 'invert(1)';
            }
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-mode');
            if (brandImage) {
                // Elimina el filtro para el modo claro
                brandImage.style.filter = 'invert(0)';
            }
            localStorage.setItem('theme', 'light');
        }
    }

    // 1. Cargar preferencia de tema al inicio
    const savedTheme = localStorage.getItem('theme');
    // Usamos savedTheme o detectamos el modo del sistema si no hay preferencia guardada
    const systemPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Prioridad: 1. Preferencia Guardada, 2. Preferencia del Sistema (si no hay guardada), 3. Light
    if (savedTheme) {
        applyTheme(savedTheme);
    } else if (systemPrefersDark) {
        // Si el usuario no ha elegido aún, usar la preferencia del sistema operativo
        applyTheme('dark'); 
    } else {
        applyTheme('light');
    }


    // 2. Evento para el botón de alternancia
    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            const currentTheme = body.classList.contains('dark-mode') ? 'light' : 'dark';
            applyTheme(currentTheme);
        });
    }

});