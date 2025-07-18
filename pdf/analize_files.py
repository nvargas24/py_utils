import os
import win32security

import datetime
import pandas as pd
from openpyxl import load_workbook

URL = r"T:\MaterialRodante\Laboratorio\Laboratorio de Electrónica"

type_files = {
    'word': ('.doc', '.docx'),
    'excel': ('.xls', '.xlsx', '.xlsm', '.xlsb'),
    'pdf': ('.pdf',),
    'powerpoint': ('.ppt', '.pptx', '.pps', '.ppsx'),
    'text': ('.txt', '.csv', '.log', '.md'),
    'images': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'),
    'compressed': ('.zip', '.rar', '.7z', '.tar', '.gz'),
    'code': ('.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.sh', '.bat'),
    'database': ('.sql', '.db', '.sqlite', '.mdb', '.accdb'),
    'cad': ('.dwg', '.dxf', '.sch'),
    'xml_json': ('.xml', '.json'),
    'outlook': ('.msg', '.eml', '.pst', '.ost'),
    'scripts': ('.ps1', '.vbs', '.reg'),
    'executables': ('.exe', '.msi'),
    'spreadsheet_other': ('.ods',),  # LibreOffice Calc
    'document_other': ('.odt',),     # LibreOffice Writer
}


def update(df, extension):
    """
    Actualiza archivo Excel 'indice de archivos.xlsx':
    - Si existe la hoja, la reemplaza.
    - Si no existe, la agrega.
    - Mantiene las demás hojas.
    """
    file_path = 'indice de archivos.xlsx'
    sheet_name = extension

    if os.path.exists(file_path):
        # Cargar el libro existente
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    else:
        # Crear nuevo archivo
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)


def extract_author(ruta):
    """
    Obteniene usuario que creo archivo
    """
    try:
        # Obtener descriptor de seguridad del archivo
        sd = win32security.GetFileSecurity(ruta, win32security.OWNER_SECURITY_INFORMATION)
        # Extraer el SID del owner
        owner_sid = sd.GetSecurityDescriptorOwner()
        # Obtener nombre legible del owner
        nombre_usuario, dominio, _ = win32security.LookupAccountSid(None, owner_sid)
        return nombre_usuario
    except win32security.error as e:
        # Ignorar el error de SID huérfano y retornar un valor por defecto
        return "Propietario no disponible"

def extract_data_file(root, name, extension):
    """
    Extrae todos los datos relevantes del archivo
    """
    dict_data_file = {}

    if name.lower().endswith(extension):
        ruta = os.path.join(root, name)
        
        dict_data_file['Nombre de archivo'] = name
        dict_data_file['Url archivo'] = f'=HYPERLINK("{ruta}", "Abrir archivo")'
        dict_data_file['Url carpeta'] = f'=HYPERLINK("{root}", "Abrir carpeta")'

        try:
            fecha_mod = os.path.getmtime(ruta)
            dict_data_file['Fecha de creación'] = datetime.datetime.fromtimestamp(fecha_mod)
        except Exception as e:
            dict_data_file['Fecha de creación'] = 'No disponible'
            print(f"[Warning] No se pudo obtener fecha de modificación: {name}")

        try:
            fecha_create = os.path.getctime(ruta)
            dict_data_file['Fecha ultima actualizacion'] = datetime.datetime.fromtimestamp(fecha_create)
        except Exception as e:
            dict_data_file['Fecha ultima actualizacion'] = 'No disponible'
            print(f"[Warning] No se pudo obtener fecha de creación: {name}")

        try:
            user_author = extract_author(ruta)
            dict_data_file['Autor'] = user_author
        except Exception as e:
            dict_data_file['Autor'] = 'No disponible'
            print(f"[Warning] No se pudo obtener el autor: {name}")
        
        return dict_data_file
        
    return None


#root: la ruta actual del directorio que se está recorriendo.
#dirs: una lista de los subdirectorios en ese directorio.
#files: una lista de los archivos en ese directorio.

for extension in type_files:
    print(f"Extension : {extension}")
    registros = []    
    for root, dirs, files in os.walk(URL):
        for name in files: # obtiene nombre de archivos disponibles
            data_file = extract_data_file(root, name, type_files[extension])
            if data_file:
                registros.append(data_file)

    df = pd.DataFrame(registros)
    print(df.info())
    update(df, extension)
