# DataClarity: Herramienta de Exploración y Visualización de Datos (MVP - Fase 1)

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/) 
[![Framework](https://img.shields.io/badge/Web%20App-Flask-orange)](https://flask.palletsprojects.com/)
[![Visualization](https://img.shields.io/badge/Graphs-Plotly-brightgreen)](https://plotly.com/)

---

## 1. 🎯 El Problema de Negocio (Business Case)

El análisis exploratorio de nuevos conjuntos de datos (EDA) es típicamente un proceso manual y lento que requiere habilidades de programación avanzadas. Esto genera una **alta fricción de adopción** para analistas o líderes de negocio que necesitan *insights* rápidos.

## 2. 💡 Solución de Producto: Carga, Limpieza y Visualización Inmediata

**DataClarity** es una aplicación web que provee una interfaz intuitiva (GUI) para que usuarios no técnicos puedan procesar y visualizar datos en minutos.

**Características Clave (Funcionalidad Actual):**

* **Ingesta Flexible:** Permite la carga de archivos en formatos CSV, Excel (`.xlsx`) y JSON.
* **Limpieza Básica (*Data Hygiene*):** Automatiza la gestión de valores faltantes (NaN) en los datos:
    * **Variables Numéricas:** Imputa los valores faltantes con la media de la columna (es decir, usa el promedio para rellenar los huecos).
    * **Variables Categóricas:** Asigna la etiqueta 'Sin Datos' a los valores nulos.
* **Estadísticas Descriptivas:** Genera un resumen estadístico (conteo, media, desviación estándar, mínimo y máximo) para las columnas numéricas.
* **Visualización Interactiva:** Soporte nativo para gráficos de dispersión (`Scatter`), barras y torta (`Pie`) a través de la librería Plotly, permitiendo la exploración de relaciones entre variables.

## 3. 🏗️ Arquitectura y Dependencias

Esta es una aplicación web desarrollada con Python, enfocada en la simplicidad para el prototipado rápido.

| Componente | Tecnología Principal | Propósito |
| :--- | :--- | :--- |
| **Framework Web** | Flask | Manejo de enrutamiento y peticiones HTTP. |
| **Procesamiento de Datos** | Pandas, Numpy | Manipulación eficiente de DataFrames y cálculos estadísticos. |
| **Visualización** | Plotly | Generación de gráficos interactivos y su integración a HTML. |
| **Base de Datos (Potencial)** | `mysql-connector-python` | Librería instalada que indica la intención futura de integración con bases de datos SQL. |

> **Nota Técnica sobre el Estado Actual:** El MVP utiliza una variable global en la aplicación (es decir, la memoria del programa) para almacenar temporalmente los datos cargados. Esto es útil para la demostración, pero será el primer punto de refactoring para asegurar la estabilidad en un entorno multiusuario real.

## 4. 🎥 Demostración Visual (¡Prioridad!)

Para que los reclutadores evalúen el producto en segundos, se recomienda añadir un GIF o un enlace a un video de 90 segundos.

* **Enfoque del Video:** Muestre la carga de un archivo -> Muestre la tabla y las estadísticas descriptivas (prueba de limpieza) -> Muestre la selección de ejes y la generación de un gráfico.
* **Guía para el GIF:** Capture el *workflow* completo de carga a visualización en un *loop* de 15 segundos.

## 5. ⏭️ Roadmap (Próxima Fase)

1.  **Ingeniería de Software:** Refactorización del código (eliminación de variables globales) y modularización de la lógica a la carpeta `src/`.
2.  **Inyección de IA:** Integración de un módulo de **Detección de Anomalías** (ML) para transformar la herramienta de exploración en un validador predictivo de calidad de datos.
3.  **Entrega Ejecutiva:** Habilitar la exportación de reportes a PDF.