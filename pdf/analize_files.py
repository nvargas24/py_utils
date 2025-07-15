import os
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

def register(root, name, extension):
    if name.lower().endswith(extension):
        ruta = os.path.join(root, name)
        try:
            fecha_mod = os.path.getmtime(ruta)
            fecha_legible = datetime.datetime.fromtimestamp(fecha_mod)
            
            return fecha_legible, ruta
        
        except Exception as e:
            print(f"Error con el archivo: {ruta}")
            return None, None
    return None, None
"""
OBS.:
root: la ruta actual del directorio que se está recorriendo.
dirs: una lista de los subdirectorios en ese directorio.
files: una lista de los archivos en ese directorio.
"""
registros = []

for root, dirs, files in os.walk(URL):
    for name in files: # obtiene nombre de archivos disponibles
        last_date, url = register(root, name, type_files['word']['extension'])
        if last_date and url:
            registros.append({
                "archivo": name,
                "ultima_modificacion": last_date,
                "ruta": url,
            })

df = pd.DataFrame(registros)
df['ruta'] = df['ruta'].apply(lambda x: f'=HYPERLINK("{x}", "Abrir archivo")')

print(df)
#print(df.info())

update(df, 'word')
