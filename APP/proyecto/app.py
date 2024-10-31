from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Variable para almacenar el DataFrame cargado
data = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global data  # Define data como global para usarlo en otras funciones

    file = request.files['file']
    if file.filename == '':
        return "El archivo no tiene nombre", 400

    # Cargar el archivo CSV en un DataFrame
    data = pd.read_csv(file)
    data_html = data.head(3).to_html()
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
    stats = calculate_statistics(data)
    
    return render_template('index.html', data=data_html, stats=stats, numeric_columns=numeric_columns)


@app.route("/generate-graph", methods=["POST"])
def generate_graph():
    data = pd.read_csv("ruta/a/tu/archivo.csv")  # Reemplaza con la ruta o la variable `data`
    selected_column = request.json.get("selected_column")
    
    # Verifica que la columna exista en el DataFrame
    if selected_column in data.columns:
        fig = px.histogram(data, x=selected_column)
        graph_html = pio.to_html(fig, full_html=False)
        return jsonify({"graph_html": graph_html})

    return jsonify({"error": "Columna no válida"}), 400



def calculate_statistics(data):
    stats = {}
    for column in data.select_dtypes(include=['number']).columns:
        stats[column] = {
            'count': data[column].count(),
            'mean': round(data[column].mean(), 2),
            'std_dev': round(data[column].std(), 2),
            'min': data[column].min(),
            'max': data[column].max()
        }
    return stats

if __name__ == '__main__':
    app.run(debug=True)
