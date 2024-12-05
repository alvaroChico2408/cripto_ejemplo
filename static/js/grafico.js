// Obtener los datos del gráfico desde el HTML
document.addEventListener('DOMContentLoaded', function() {
    const tiempos = JSON.parse(document.getElementById('tiempos').textContent);
    const precios_simulados = JSON.parse(document.getElementById('precios_simulados').textContent);

    // Crear el gráfico
    var trace1 = {
        x: tiempos,
        y: precios_simulados,
        type: 'scatter'
    };

    var data = [trace1];

    var layout = {
        title: 'Precio Simulado del Bitcoin',
        xaxis: {
            title: 'Tiempo'
        },
        yaxis: {
            title: 'Precio en USD'
        }
    };

    Plotly.newPlot('grafico', data, layout);
});
