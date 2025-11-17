from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
# Importamos la lógica de negocio modularizada
from src.data_processor import process_uploaded_file, calculate_statistics 

# --- CONFIGURACIÓN DE APLICACIÓN SEGURA ---
app = Flask(__name__)
# CLAVE CRÍTICA: Necesaria para cifrar las 'sessiones' de cada usuario. 
# Esto elimina el riesgo de la variable global y la inseguridad. 
# IMPORTANTE: Reemplace este valor con una cadena larga y aleatoria en producción.
app.config['SECRET_KEY'] = 'ESTE_DEBE_SER_UN_STRING_LARGO_Y_SECRETO_QUE_NADIE_PUEDA_ADIVINAR_AumentandoLaSeguridad12345'

# --- FUNCIONES DE SOPORTE ---
def get_data_from_session(): 
    """Recupera el DataFrame de la sesión del usuario (si existe)."""
    # session.get('data') retorna el JSON del DF o None
    data_json = session.get('data')
    if data_json:
        # Se convierte el JSON de vuelta a DataFrame de Pandas
        return pd.read_json(data_json, orient='split')
    return None

# --- RUTAS WEB (CONTROLADORES) ---

@app.route('/')
def home():
    # Si no hay datos cargados en la sesión, se limpia la vista de gráficos
    if not session.get('data'):
        return render_template('index.html')
    
    # Si hay datos, se recuperan las estadísticas para mostrarlas
    data = get_data_from_session()
    stats = calculate_statistics(data)
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()
    all_columns = data.columns.tolist()

    return render_template(
        'index.html', 
        data=data.head(10).to_html(),
        stats=stats, 
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        all_columns=all_columns
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    
    # Se utiliza request.files.get('file') para que funcione como antes.
    file = request.files.get('file')  
    
    if file is None or file.filename == '':
        return "Por favor, selecciona un archivo CSV, Excel o JSON", 400

    try:
        # Se pasa el archivo a la función modularizada para procesar.
        data, numeric_columns, categorical_columns = process_uploaded_file(file, file.filename)
        
        # Guardamos el DataFrame PROCESADO en la sesión del usuario como JSON (orient='split' es robusto)
        session['data'] = data.to_json(orient='split')
        
        # Redireccionamos a la ruta home (/) para que se ejecute y muestre la tabla
        return redirect(url_for('home'))

    except Exception as e:
        # En caso de error, limpiamos la sesión para forzar al usuario a empezar de nuevo.
        session.pop('data', None)
        return f"Error al leer o procesar el archivo: {str(e)}", 500


@app.route('/select-graph', methods=['POST'])
def select_graph():
    data = get_data_from_session()
    if data is None:
        return redirect(url_for('home')) # Redirige si no hay datos.

    graph_type = request.form.get('graph_type')
    
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()

    return render_template(
        'index.html',
        graph_type=graph_type,
        numeric_columns=numeric_columns,
        all_columns=data.columns.tolist(),
        categorical_columns=categorical_columns,
        data=data.head(5).to_html(),
        stats=calculate_statistics(data)
    )

@app.route('/generate-graph', methods=['POST'])
def generate_graph():
    data = get_data_from_session()
    if data is None:
        return redirect(url_for('home')) # Redirige si no hay datos.
    
    # ... El resto de la lógica de generación de gráficos permanece igual ...
    graph_type = request.form.get('graph_type')
    x_column = request.form.get('x_column')
    y_column = request.form.get('y_column') if graph_type != 'pie' else None
    
    
    if not x_column or x_column not in data.columns:
        return "Por favor, selecciona una columna válida para el eje X", 400
    
    if y_column and y_column not in data.columns:
        return "Por favor, selecciona una columna válida para el eje Y", 400

    try:
        if graph_type == 'scatter':
            fig = px.scatter(data, x=x_column, y=y_column)        
        elif graph_type == 'bar':
            fig = px.bar(data, x=x_column, y=y_column)
        elif graph_type == 'pie':
            fig = px.pie(data, names=x_column)
        else:
            return "Tipo de gráfico no soportado", 400

        graph_html = pio.to_html(fig, full_html=False)

    
    except Exception as e:
        return f"Error al generar el gráfico: {str(e)}", 500

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

# ... (La ruta /faqs y el main se dejan iguales) ...

@app.route("/faqs")
def faqs():
    # ... (contenido de faqs.html) ...
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




# --- NUEVA RUTA: RESET DE DATOS --- 
@app.route('/reset-data') # Ruta para limpiar los datos de la sesión
def reset_data(): 
    """Limpia el DataFrame de la sesión del usuario y redirige a la página de inicio."""
    # Acción: Eliminar la clave 'data' de la sesión. Si no existe, no hace nada (seguro).
    session.pop('data', None)
    # Redireccionamos a la función home (/) para recargar la página limpia
    return redirect(url_for('home')) # Redirige a la página de inicio limpia


if __name__ == '__main__':
    app.run(debug=True)