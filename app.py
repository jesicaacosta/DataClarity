from flask import Flask, render_template, request  #  crear la app y manejar solicitudes html 
import pandas as pd  # manejo de datos dataframes
import plotly.express as px  # Generar graficos interactivos
import plotly.io as pio  # Convertir garficos de Plotly a HTML
#from weasyprint import HTML  #generar archivos PDF a partir de contenido HTML.

app = Flask(__name__)

# Variable global para almacenar el DF cargado
data = None

@app.route('/')
def home():
    return render_template('index.html')  # Muestra la pagina principal

@app.route('/upload', methods=['POST'])
def upload_file():
    global data  #para hacer quye data sea global
    file = request.files['file']  # Archivo subido 
    if file.filename == '':
        return "Por favor, selecciona un archivo CSV o Excel", 400

    #Leer el archivo
    data = pd.read_csv(file)
    data_html = data.head(5).to_html()
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist() #solo selecciona columnas numericas
    all_columns = data.columns.tolist() #lista de todas las columnas
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()  # columnas no numericas
    
    #Limpieza de datos
    nulos= data.isnull().sum()

    if nulos.any():  #  si hay nulos en la vaiable nulos
        for column in numeric_columns:  # Itera sobre cada elemen numeric columns
            data[column] = data[column].fillna(data[column].mean())  # Reemplaza los valores nulos con la media del df original


    # llama funcion las estadist del DF cargado
    stats = calculate_statistics(data)
    
    return render_template( #retorna todo para poder utilizarlo
        'index.html', 
        data=data_html, 
        stats=stats, 
        numeric_columns=numeric_columns, # columnasn numericas
        categorical_columns=categorical_columns,  # Añadimos las columnas categóricas
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


@app.route('/select-graph', methods=['POST'])
def select_graph():
    global data
    if data is None:
        return "No hay datos cargados", 400

    graph_type = request.form.get('graph_type')
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist() #

    return render_template(
        'index.html',
        graph_type=graph_type,
        numeric_columns=numeric_columns,
        all_columns=data.columns.tolist(),
        categorical_columns=categorical_columns,
        data=data.head(5).to_html()
    )



@app.route('/generate-graph', methods=['POST'])
def generate_graph():
    global data
    if data is None:
        return "No hay datos cargados", 400

    graph_type = request.form.get('graph_type')
    x_column = request.form.get('x_column')
    y_column = request.form.get('y_column') if graph_type != 'pie' else None

    if not x_column:
        return "Por favor, selecciona una columna para el eje X", 400

    try:
        if graph_type == 'scatter': #graf de dispersion
            fig = px.scatter(data, x=x_column, y=y_column)        
        elif graph_type == 'bar': #
            fig = px.bar(data, x=x_column, y=y_column)
        elif graph_type == 'pie': #graf de torta, solo con una columna
            fig = px.pie(data, names=x_column)
        else:
            return "Tipo de gráfico no soportado", 400

        graph_html = pio.to_html(fig, full_html=False)
    except Exception as e:
        return f"Error al generar el gráfico: {str(e)}", 500

    return render_template(
        'index.html',
        graph_html=graph_html,
        x_column=x_column,
        y_column=y_column,
        graph_type=graph_type,
        data=data.head(5).to_html(),
        numeric_columns=data.select_dtypes(include=['number']).columns.tolist(),
        all_columns=data.columns.tolist(),
        categorical_columns= data.columns.to_list(),
        stats=calculate_statistics(data)
    )




if __name__ == '__main__':
    app.run(debug=True)
