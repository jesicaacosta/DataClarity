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
    return render_template('index.html')  # muestra la pagina principal

@app.route('/upload', methods=['POST'])
def upload_file():
    global data  # hace quye data sea global
    file = request.files['file']  # Archivo subido 
    if file.filename == '':
        return "Por favor, selecciona un archivo CSV, Excel o JSON", 400
    #Agregar funcion volver index.html

    # Detectar y leer archivo
    try:
        if file.filename.endswith('.xlsx'):
            data = pd.read_excel(file)
        elif file.filename.endswith('.json'):
            data = pd.read_json(file)
        else:
            data = pd.read_csv(file)
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}", 500
                
    #columnas 
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist() #solo selecciona columnas numericas
    all_columns = data.columns.tolist() #lista de todas las columnas
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()  # columnas no numericas
        
    #Limpieza de datos
    for column in numeric_columns:
        data[column] = data[column].fillna(data[column].mean())   
        
    for column in categorical_columns:
        data[column] = data[column].fillna('Sin Datos')
    #recomendado hacer la limpieza de datos con machine learning, por moda, tendencias
            
    data_html = data.head(10).to_html()
    stats = calculate_statistics(data)
    
    return render_template( #retorna todo para poder utilizarlo
        'index.html', 
        data=data_html, 
        stats=stats, 
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        all_columns=all_columns
    )
    
    

   
#FUNION CALCULAR ESTADISTICAS
def calculate_statistics(data):
    stats = {}
    for column in data.select_dtypes(include=['number']).columns:
        stats[column] = {
            'count': data[column].count(),  # Cantidad de valores no nulos 
            'mean': round(data[column].mean(), 2),  # Promedio redondeado a dos decimales
            'std_dev': round(data[column].std(), 2),  # Desviacion estandar
            'min': data[column].min(),  # Valor min
            'max': data[column].max()   # Valor max
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
    
#obtener valores del formulario
    graph_type = request.form.get('graph_type')
    x_column = request.form.get('x_column')
    y_column = request.form.get('y_column') if graph_type != 'pie' else None
    
    
    # Validar que las columnas seleccionadas existan
    if not x_column or x_column not in data.columns:
        return "Por favor, selecciona una columna válida para el eje X", 400
    
    if y_column and y_column not in data.columns:
        return "Por favor, selecciona una columna válida para el eje Y", 400

    try:
        #generar grafico
        if graph_type == 'scatter': #graf de dispersion
            fig = px.scatter(data, x=x_column, y=y_column)        
        elif graph_type == 'bar': #
            fig = px.bar(data, x=x_column, y=y_column)
        elif graph_type == 'pie': #graf de torta, solo con una columna
            fig = px.pie(data, names=x_column)
        else:
            return "Tipo de gráfico no soportado", 400

#convertir grafico a HTML
        graph_html = pio.to_html(fig, full_html=False)

    
    except Exception as e:
        return f"Error al generar el gráfico: {str(e)}", 500

        # Seleccionar columnas válidas para mostrar
    columns_to_display = [col for col in [x_column, y_column] if col]
    data_text = data[columns_to_display].to_string(index=False)
    
    
    return render_template(
       'index.html',
        graph_html=graph_html,
        x_column=x_column,
        y_column=y_column,
        graph_type=graph_type,
        data=data.head(5).to_html(),
        data_text=data_text,
        numeric_columns=data.select_dtypes(include=['number']).columns.tolist(),
        all_columns=data.columns.tolist(),
        categorical_columns=data.select_dtypes(include=['object']).columns.tolist(),
        stats=calculate_statistics(data)
    )

#PAGINA FAQS
@app.route("/faqs")
def faqs():
    preguntas = [
        "¿Qué tipos de archivos puedo subir a la plataforma?",
        "¿Mis datos están seguros?",
        "¿Cómo visualizo un gráfico interactivo?",
        "¿Qué herramientas están disponibles para analizar datos?",
        "¿Puedo exportar gráficos y estadísticas?",
        "¿Cuáles son las opciones de respaldo de datos?",
        "¿Puedo cargar múltiples archivos a la vez?",
        "¿Hay un límite en el tamaño del archivo que puedo subir?",
        "¿Cómo selecciono el tipo de gráfico que quiero generar?",
        "¿Puedo guardar mi progreso y continuar más tarde?",
        "¿Se admiten datos categóricos y numéricos?",
        "¿Cómo funciona el análisis de tendencias?",
        "¿Qué sucede si mi archivo tiene datos incompletos?",
        "¿Puedo obtener soporte técnico?",
        "¿La plataforma es compatible con dispositivos móviles?"
    ]
    respuestas = [
        "Puedes subir archivos en formato CSV, XLSX y JSON.",
        "Sí, implementamos medidas de seguridad avanzadas para proteger tu información.",
        "Selecciona las columnas deseadas y elige el tipo de gráfico en nuestra interfaz.",
        "Ofrecemos gráficos, estadísticas básicas y más.",
        "Sí, puedes descargar gráficos en formato PNG y estadísticas en PDF.",
        "Pronto tendremos integración con Google Drive para respaldos automáticos.",
        "Por el momento, solo un archivo a la vez es permitido.",
        "No recomendamos archivos mayores a 50 MB para un mejor rendimiento.",
        "Elige entre gráficos de dispersión, barras y sectores.",
        "Sí, tu cuenta guarda los datos cargados para su posterior análisis.",
        "Sí, ambos tipos de datos son compatibles con nuestras herramientas.",
        "Analiza patrones y comportamientos directamente desde los gráficos.",
        "La plataforma ignora valores nulos en los cálculos.",
        "Contáctanos a través de nuestra sección de soporte para ayuda inmediata.",
        "Sí, nuestra plataforma es responsive y funciona en todos los dispositivos."
    ]
    return render_template("faqs.html", preguntas=preguntas, respuestas=respuestas)


if __name__ == '__main__':
    app.run(debug=True)
