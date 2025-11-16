#Este archivo contiene las funciones que trabajan directamente con el dataframe de Pandas, extrayéndolas de app.py. 

import pandas as pd
import numpy as np

# 1. FUNCIÓN PARA CARGA Y LIMPIEZA DE DATOS (CORE DEL PRODUCTO)
def process_uploaded_file(file_data, filename):
    """Carga y aplica limpieza básica de datos (imputación)."""
    
    # 1. Detección y Lectura del Archivo
    if filename.endswith('.xlsx'):
        data = pd.read_excel(file_data)
    elif filename.endswith('.json'):
        data = pd.read_json(file_data)
    else:
        # Asume CSV por defecto si no es json o xlsx
        data = pd.read_csv(file_data)
    
    # 2. Tipos de Columnas
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
    categorical_columns = data.select_dtypes(include=['object']).columns.tolist()
    
    # 3. Limpieza de datos (Imputación por media o 'Sin Datos')
    for column in numeric_columns:
        # Aquí se usa el método de imputación actual (media)
        data[column] = data[column].fillna(data[column].mean())
        
    for column in categorical_columns:
        data[column] = data[column].fillna('Sin Datos')
        
    # Retorna el DataFrame limpio y las listas de columnas
    return data, numeric_columns, categorical_columns

# 2. FUNCIÓN PARA CÁLCULO DE ESTADÍSTICAS
def calculate_statistics(data):
    """Calcula las estadísticas descriptivas para columnas numéricas."""
    stats = {}
    for column in data.select_dtypes(include=['number']).columns:
        stats[column] = {
            'count': data[column].count(),  # Cantidad de valores no nulos 
            'mean': round(data[column].mean(), 2),  # Promedio
            'std_dev': round(data[column].std(), 2),  # Desviación estándar
            'min': data[column].min(),  # Mínimo
            'max': data[column].max()   # Máximo
        }
    return stats

