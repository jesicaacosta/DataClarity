from flask import Flask, render_template, request, jsonify  # Flask para crear la app y manejar solicitudes
import pandas as pd  # Manejo de datos
import plotly.express as px  # Generar gráficos interactivos
import plotly.io as pio  # Convertir gráficos de Plotly a HTML

app = Flask(__name__)

# Variable global para almacenar el DataFrame cargado
data = None

@app.route('/')
def home():
    return render_template('index.html')  # Muestra la página principal

@app.route('/upload', methods=['POST'])
def upload_file():
    global data  #para hacer quye data sea global
    file = request.files['file']  # Archivo subido 
    if file.filename == '':
        return "Por favor, selecciona un archivo CSV o Excel", 400

    #lee el archivo
    data = pd.read_csv(file)
    data_html = data.head(5).to_html()
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist() #solo selecciona columnas numericas
    all_columns = data.columns.tolist()

    # Calcula las estadísticas del DataFrame cargado
    stats = calculate_statistics(data)

    return render_template(
        'index.html', 
        data=data_html, 
        stats=stats, 
        numeric_columns=numeric_columns, # columnasn numericas
        all_columns=all_columns  
    )

def calculate_statistics(data):
    stats = {}
    for column in data.select_dtypes(include=['number']).columns:
        stats[column] = {
            'count': data[column].count(),  # Cantidad de valores no nulos 
            'mean': round(data[column].mean(), 2),  # Promedio redondeado a dos decimales
            'std_dev': round(data[column].std(), 2),  # Desviación estándar
            'min': data[column].min(),  # Valor mínimo
            'max': data[column].max()   # Valor máximo
        }
    return stats

@app.route('/generate-graph', methods=['POST'])
def generate_graph():
    global data
    if data is None:
        return "No hay datos cargados", 400

    x_column = request.form['x_column']
    y_column = request.form['y_column']

    if x_column not in data.columns or y_column not in data.columns:
        return "Columnas seleccionadas no válidas", 400

    # Gráfico de dispersión
    fig1 = px.scatter(data, x=x_column, y=y_column, title=f'Gráfico de Dispersión {x_column} vs {y_column}')
    graph_html1 = pio.to_html(fig1, full_html=False)
    
    # Gráfico de barras
    fig2 = px.bar(data, x=x_column, y=y_column, title=f'Gráfico de Barras {x_column} vs {y_column}', color=y_column)
    graph_html2 = pio.to_html(fig2, full_html=False)

    # Gráfico de sectores 10 
    top_10 = data.nlargest(10, y_column)
    fig_top = px.pie(top_10, names=x_column, values=y_column, title=f'Valores mas altos de {y_column} en relacion a {x_column}')
    graph_html_top = pio.to_html(fig_top, full_html=False)

    # Renderizar en `graficos.html`
    return render_template(
        'graficos.html',
        graph1=graph_html1,
        graph2=graph_html2,
        fig_top=graph_html_top,
        x_column=x_column,
        y_column=y_column
    )

if __name__ == '__main__':
    app.run(debug=True)
