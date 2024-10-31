/*
Manejador de evento para el botón de generar gráfico
document.getElementById("generate-graph").addEventListener("click", function(event) {
    event.preventDefault();  // Evita que el formulario se envíe automáticamente

    const selectedColumn = document.getElementById("selected_column").value;  // Obtiene la columna seleccionada

    // Envía el valor de la columna seleccionada al servidor
    fetch("/generate-graph", {  // Asegúrate de que esta ruta coincide con la de app.py
        method: "POST",  // Especifica que se enviará una solicitud POST
        headers: {
            "Content-Type": "application/json"  // Indica que el contenido enviado es JSON
        },
        body: JSON.stringify({ selected_column: selectedColumn })  // Convierte el objeto JavaScript a JSON
    })
    .then(response => response.json())  // Espera una respuesta en formato JSON
    .then(data => {
        // Si se recibe el HTML del gráfico
        if (data.graph_html) {
            const graphDiv = document.getElementById("graph");  // Cambia esto a 'graph' ya que es donde se mostrará
            graphDiv.innerHTML = data.graph_html;  // Inserta el HTML del gráfico en el contenedor
            graphDiv.style.display = "block";  // Asegura que el contenedor del gráfico sea visible
        } else {
            // Si no se recibe un gráfico válido, muestra un error en la consola
            console.error("Error: ", data.error || "No se pudo generar el gráfico.");
        }
    })
    .catch(error => {
        // Captura y muestra cualquier error que ocurra durante la solicitud
        console.error("Error al generar el gráfico:", error);
    });
});
*/



// Manejador de evento para el botón de generar gráfico
// Manejador de evento para el botón de generar gráfico
document.getElementById("generate-graph").addEventListener("click", function(event) {
    event.preventDefault(); // Evita que el formulario se envíe de forma predeterminada

    // Enviar una solicitud para generar el gráfico sin seleccionar columna
    fetch("/generate-graph", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        // Muestra el gráfico devuelto por el servidor
        if (data.graph_html) {
            const graphDiv = document.getElementById("graph");
            graphDiv.innerHTML = data.graph_html;
            graphDiv.classList.remove("hidden"); // Muestra el gráfico
        } else {
            console.error("Error: ", data.error || "No se pudo generar el gráfico.");
        }
    })
    .catch(error => {
        console.error("Error al generar el gráfico:", error);
    });
});
