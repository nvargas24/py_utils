"""
rename_format_file.py
-----------

Descripción general:
Este módulo se encarga de renombrar archivos .doc y .docx
para ajustar al formato :  'LS-MR-CT-R-000 [nombre de archivo]'

Autor: Ing. Vargas Nahuel
Fecha: 2025-04-21
Versión: 1.0.0
Licencia: MIT (u otra)
"""
import os
import re

# Ruta de la carpeta
carpeta = None

# Recorrer todos los archivos en la carpeta
for archivo in os.listdir(carpeta): 
    if archivo.endswith('.doc') or archivo.endswith('.docx'):
        # Si el archivo comienza con 'Nota'
        if archivo.startswith('Nota'):
            # Crear nuevo nombre con el prefijo añadido
            nuevo_nombre = 'LS-MR-CT-R-000 ' + archivo
            # Obtener la ruta completa de los archivos
            ruta_vieja = os.path.join(carpeta, archivo)
            ruta_nueva = os.path.join(carpeta, nuevo_nombre)
            # Renombrar el archivo
            os.rename(ruta_vieja, ruta_nueva)
            print(f'Renombrado: {ruta_vieja} a {ruta_nueva}')
        else:
            print(f'Sin cambios: {archivo}')
    else:
        print(f'Archivo no considerado: {archivo}')
