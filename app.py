from flask import Flask, render_template, request, jsonify  # bibliotecas de Flask
import pandas as pd  #
import plotly.express as px  #  plotly para la visualizacion de grafuicos
import plotly.io as pio  # funciones de entrada/salida de plotly


app = Flask(__name__)  # crea una instancia de la aplicacion Flask

# Variable global para almacenar el df cargado
data = None

@app.route('/')  #  ruta principal de la app
def home():
    return render_template('index.html')  # Renderiza/llama la plantilla index.html

@app.route('/upload', methods=['POST'])  # Ruta para manejar la subida de archivos
def upload_file():
    global data  # Permite acceder a la variable 'data' en otras funciones

    file = request.files['file']  # Obtiene el archivo del formulario
    if file.filename == '':
        return "Por favor, selecciona un archivo CSV o Excel", 400  # Respuesta de error si no se selecciona un archivo

    # Carga el archivo CSV en un DataFrame
    data = pd.read_csv(file)
    data_html = data.head(3).to_html()  # Convierte a html y muestra  las primeras tres filas del df subido
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()  # Obtiene las columnas nmericas
    stats = calculate_statistics(data)  # Calcula las estadisticas basicas del df
    
    # renderiza de nuevo la plantilla con los datos cargados y las estadisticas
    return render_template('index.html', data=data_html, stats=stats, numeric_columns=numeric_columns)


# resumen estadstico basico de un DF de pandas
def calculate_statistics(data):
    stats = {}
    for column in data.select_dtypes(include=['number']).columns: # filtra solo las columnas num
        stats[column] = {
            'count': data[column].count(),#cuenta el nro de valores no nulos en la columna
            'mean': round(data[column].mean(), 2),#calcula promedio y redondea el resultado a 2 decimale
            'std_dev': round(data[column].std(), 2), #calcula la desviación estand de los valores de la columna y redondea el resultado a dos decimales
            'min': data[column].min(),
            'max': data[column].max()
        }
    return stats 
#devuelve el diccionario stats que contiene todas las estad calculadas para cada columna num



'''

1- grafico x
2- grafico y
3- onmbre para el grafico x
4- onmbre para el grafico y
5- 



def view_statistics(data):
     for column in data.select_dtypes(include=['number']).columns: # filtra solo las columnas num
        stats[column] = {
        }
    return grafico''' 


if __name__ == '__main__':
    app.run(debug=True)
    
    
    ''' 
 

#funcion pa aestadistica sbasicas
def calculate_statistics(data):
    stats = {}  # Inicializa un diccionario para almacenar las estadist
    for column in data.select_dtypes(include=['number']).columns:
        # Calcula y almacena estadist para cada columna nnmerica
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

'''