// Manejador de evento para el botón de generar gráfico
document.getElementById("generate-graph").addEventListener("click", function() {
    const selectedColumn = document.getElementById("selected_column").value;

    // Envía el valor de la columna seleccionada al servidor
    fetch("/update_graph", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ selected_column: selectedColumn })
    })
    .then(response => response.text())
    .then(graphHtml => {
        // Inserta el gráfico en el contenedor designado
        document.getElementById("graph-container").innerHTML = graphHtml;
    })
    .catch(error => {
        console.error("Error:", error);
    });
});


// Para el boton de generar grafico 
document.getElementById("generate-graph").addEventListener("click", function(event) {
    event.preventDefault(); // Evita que el formulario se envíe de forma predeterminada

    // Obtiene la columna seleccionada
    const selectedColumn = document.getElementById("selected_column").value;

    // Enviar el valor seleccionado al servidor para generar el gráfico
    fetch("/generate-graph", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ selected_column: selectedColumn })
    })
    .then(response => response.json())
    .then(data => {
        // Mostrar el gráfico devuelto por el servidor
        const graphDiv = document.getElementById("graph");
        graphDiv.innerHTML = data.graph_html;
        graphDiv.style.display = "block"; // Muestra el gráfico
    })
    .catch(error => {
        console.error("Error al generar el gráfico:", error);
    });
});
