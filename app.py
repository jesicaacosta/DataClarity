from flask import Flask, render_template, request, jsonify  # flask para crear la app y manejar solicitudes
import pandas as pd  # 
import plotly.express as px  #  generar graficos interactivos
import plotly.io as pio  #  convertir graficos de Plotly a HTML


app = Flask(__name__)

# Variable global para almacenar el DataFrame cargado
data = None

@app.route('/')
def home():
    return render_template('index.html') #muestra la pagina principal

@app.route('/upload', methods=['POST'])
def upload_file():
    global data
    file = request.files['file'] #archivo subido 
    if file.filename == '':
        return "Por favor, selecciona un archivo CSV o Excel", 400

    data = pd.read_csv(file)
    data_html = data.head(3).to_html()
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
    all_columns = data.columns.tolist()

    #calcula las estdisicas del df cargado
    stats = calculate_statistics(data)

    return render_template(
        'index.html', 
        data=data_html, 
        stats=stats, 
        numeric_columns=numeric_columns,
        all_columns=all_columns  # Enviar todas las columnas para eje X
    )

def calculate_statistics(data):
    stats = {}
    for column in data.select_dtypes(include=['number']).columns:
        stats[column] = {
            'count': data[column].count(), #cant valores no nulos 
            'mean': round(data[column].mean(), 2), #pronedio redondeado a dos decimales
            'std_dev': round(data[column].std(), 2), 
            'min': data[column].min(),
            'max': data[column].max()
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


    #Grafico de dispersion 
    fig1 = px.scatter(data, x=x_column, y=y_column, title=f'Gráfico de Dispersion {x_column} vs {y_column}')
    graph_html1 = pio.to_html(fig1, full_html=False)
    
    #Grafico de barras 
    fig2 = px.bar(data, x=x_column, y=y_column, title=f'Gráfico de barras  {x_column} vs {y_column} ', color = y_column)
    graph_html2 = pio.to_html(fig2, full_html=False)
    #full_html=False: GRAFICO sin la estructura completa de un documento HTML.

    #Grafico de sectores 
    fig3 = px.pie(data, names=x_column, values=y_column, title=f'Gráfico de sectores de {x_column} vs {y_column}')
    graph_html3 = pio.to_html(fig3, full_html=False)


    return render_template(
        'index.html',
        data=data.head(3).to_html(),
        numeric_columns=data.select_dtypes(include=['number']).columns.tolist(),
        all_columns=data.columns.tolist(),
        graph1=graph_html1,
        graph2=graph_html2,
        graph3= graph_html3
        
    )

if __name__ == '__main__':
    app.run(debug=True)
