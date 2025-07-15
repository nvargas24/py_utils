import os
import win32security

import datetime
import pandas as pd

URL = r"T:\MaterialRodante\Laboratorio\Laboratorio de Electrónica"

type_files = {
    'word': {
        'name_sheet': "Word",
        'extension': ('.doc', 'docx')
    },

    'excel' : {
        'name_sheet': "Excel",
        'extension': ('.xls', 'xlsx')
    },

    'pdf' : {
        'name_sheet': "Pdf",
        'extension': '.pdf'
    }    
}

def update(df, extension):
    """
    Actualiza excel con indice de todos los formatos disponibles
    """
    df.to_excel('indice de archivos.xlsx', 
                index=False, 
                sheet_name=type_files[extension]['name_sheet']
    )

def extract_author(ruta):
    # Obtener descriptor de seguridad del archivo
    sd = win32security.GetFileSecurity(ruta, win32security.OWNER_SECURITY_INFORMATION)
    # Extraer el SID del owner
    owner_sid = sd.GetSecurityDescriptorOwner()
    # Obtener nombre legible del owner
    nombre_usuario, dominio, _ = win32security.LookupAccountSid(None, owner_sid)

    return nombre_usuario

def extract_data_file(root, name, extension):
    dict_data_file = {}

    if name.lower().endswith(extension):
        ruta = os.path.join(root, name)
        try:
            user_author = extract_author(ruta)
            fecha_mod = os.path.getmtime(ruta)
            fecha_create = os.path.getctime(ruta)

            dict_data_file['Nombre de archivo'] = name
            dict_data_file['Fecha de creación'] = datetime.datetime.fromtimestamp(fecha_mod)
            dict_data_file['Fecha ultima actualizacion'] = datetime.datetime.fromtimestamp(fecha_create)
            dict_data_file['Autor'] = user_author
            dict_data_file['Url'] = f'=HYPERLINK("{ruta}", "Abrir archivo")'

            return dict_data_file
        
        except Exception as e:
            print(f"Error con el archivo: {ruta}")
            return None
    return None

"""
OBS.:
root: la ruta actual del directorio que se está recorriendo.
dirs: una lista de los subdirectorios en ese directorio.
files: una lista de los archivos en ese directorio.
"""
registros = []

for root, dirs, files in os.walk(URL):
    for name in files: # obtiene nombre de archivos disponibles
        data_file = extract_data_file(root, name, type_files['word']['extension'])
        if data_file:
            registros.append(data_file)

df = pd.DataFrame(registros)

print(df)
print(df.info())

update(df, 'word')
