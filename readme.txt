app.py

def calculate_statistics(data):
    recibe el df data
    Calcula estadist conteo, media, desviac estandar, min y max
    Devulve un diccionario con las estadísticas clave, con columna y estad.
    


graph_html contiene el gráfico en HTML, que pasaremos al index.html.


---------------------------

Aplicación Flask:

El núcleo de toda aplicación es una instancia de Flask. Define rutas, configura la aplicación y ejecuta el servidor.
Rutas:

Se definen con el decorador @app.route. Cada ruta está asociada con una función que maneja la lógica para esa URL.
Contexto:

Request Context: Contiene información específica de la solicitud (datos del cliente, formularios, etc.).
Application Context: Maneja la configuración y recursos compartidos.
Plantillas (Jinja2):

Permite separar la lógica de la aplicación del diseño visual, usando expresiones, bucles y condicionales.
Manejo de métodos HTTP:

Flask soporta métodos como GET, POST, PUT, DELETE.
Define qué método se permite en cada ruta para manejar formularios o API RESTful.
Redirección y URL:

Redirige a otras rutas usando redirect y genera URLs dinámicas con url_for.
Manejo de errores:

Permite definir páginas personalizadas para errores comunes como 404 (Página no encontrada) o 500 (Error del servidor).
Ciclo de Vida de una Solicitud
Cliente hace una solicitud (HTTP).
Servidor Flask procesa la solicitud:
Match de la URL con una ruta.
Ejecuta la función asociada.
Devuelve una respuesta (HTML, JSON, etc.).
El navegador muestra la respuesta.

----------------------------
JINJA2:

{{ ... }}:
Es la sintaxis de Jinja2 para inyectar variables o expresiones en una plantilla HTML. 
Lo que esté dentro de {{ ... }} se reemplaza por el valor de la variable o resultado de 
la expresión cuando se renderiza la página.

|safe:
Es un filtro de Jinja2 que indica que el contenido es seguro y no debe escaparse. Por defecto, Jinja2 
escapa cualquier contenido HTML para evitar ataques de XSS (Cross-Site Scripting).
Sin |safe, el navegador mostraría el código HTML como texto literal.
Con |safe, el contenido se interpreta como HTML y se renderiza correctamente en la página.

--- ---GRAFICOS 

px.scatter :Genera un gráfico de dispersión (scatter plot).
fig1 = px.scatter(data, x='edad', y='altura', title='Gráfico de Edad vs Altura')
data: El conjunto de datos (por ejemplo, un DataFrame de pandas) que contiene la información a graficar.
x: Nombre de la columna para el eje X.
y: Nombre de la columna para el eje Y.
title: El título del gráfico.

