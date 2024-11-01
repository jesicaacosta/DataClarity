from flask import Flask, render_template, request, jsonify  # Importa las bibliotecas necesarias de Flask
import pandas as pd  # Importa pandas para manejar datos en DataFrames
import plotly.express as px  # Importa plotly para la visualización de gráficos
import plotly.io as pio  # Importa funciones de entrada/salida de plotly


app = Flask(__name__)  # Crea una instancia de la aplicación Flask

# Variable global para almacenar el DataFrame cargado
data = None

@app.route('/')  # Define la ruta principal de la aplicación
def home():
    return render_template('index.html')  # Renderiza la plantilla index.html

@app.route('/upload', methods=['POST'])  # Ruta para manejar la subida de archivos
def upload_file():
    global data  # Permite acceder a la variable 'data' en otras funciones

    file = request.files['file']  # Obtiene el archivo del formulario
    if file.filename == '':
        return "Por favor, selecciona un archivo CSV o Excel", 400  # Respuesta de error si no se selecciona un archivo

    # Carga el archivo CSV en un DataFrame
    data = pd.read_csv(file)
    data_html = data.head(3).to_html()  # Convierte y muestra  las primeras tres filas del DataFrame a HTML
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()  # Obtiene las columnas numéricas
    stats = calculate_statistics(data)  # Calcula las estadísticas básicas del DataFrame
    
    # Renderiza de nuevo la plantilla con los datos cargados y las estadísticas
    return render_template('index.html', data=data_html, stats=stats, numeric_columns=numeric_columns)


# resumen estadstico basico de un DF de pandas
def calculate_statistics(data):
    stats = {}
    for column in data.select_dtypes(include=['number']).columns: # filtra solo las columnas num
        stats[column] = {
            'count': data[column].count(),#Cuenta el número de valores no nulos en la columna
            'mean': round(data[column].mean(), 2),#Calcula promedio y redondea el resultado a dos decimale
            'std_dev': round(data[column].std(), 2), #Calcula la desviación estándar de los valores de la columna y redondea el resultado a dos decimales."
            'min': data[column].min(),
            'max': data[column].max()
        }
    return stats 
#devuelve el diccionario stats que contiene todas las estad calculadas para cada columna num





if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# Función para calcular estadísticas básicas
def calculate_statistics(data):
    stats = {}  # Inicializa un diccionario para almacenar las estadísticas
    for column in data.select_dtypes(include=['number']).columns:
        # Calcula y almacena estadísticas para cada columna numérica
        stats[column] = {
            'count': data[column].count(),  # Conteo de valores
            'mean': round(data[column].mean(), 2),  # Media
            'std_dev': round(data[column].std(), 2),  # Desviación estándar
            'min': data[column].min(),  # Valor mínimo
            'max': data[column].max()  # Valor máximo
        }
    return stats  # Devuelve el diccionario de estadísticas

if __name__ == '__main__':
    app.run(debug=True)  # Ejecuta la aplicación en modo depuración
