import pdfplumber
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from file import read_cfg as cfg
import pprint
import re

def extraer_tablas_pdf(ruta_pdf):
    datos = []
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina_num, pagina in enumerate(pdf.pages):
            tablas = pagina.extract_tables()
            for tabla_num, tabla in enumerate(tablas):
                # Elimina None de cada fila
                tabla_limpia = [
                    [celda for celda in fila if celda is not None]
                    for fila in tabla if fila is not None
                ]
                
                # combina listas y sublistas en un str
                str_table = '\n'.join(' '.join(map(str, fila)) for fila in tabla_limpia)
                str_limpio = re.sub(r'\s+', ' ', str_table)

                datos.append({
                    "pagina": pagina_num + 1,
                    "tabla": tabla_num + 1,
                    "contenido": str_limpio
                })

    return datos

def struct_tablas(datos):
    tablas = {}

    for tabla_info in datos:
        tablas[f"Pag{tabla_info['pagina']}_Table{tabla_info['tabla']}"] = tabla_info['contenido']

    return tablas

def search_data(data):
    dict_data = {}
    patron = r'MODULO\s+(\w+).*?SISTEMA\s+(\w+).*?N° SERIE\s*(\w+)?\s*PRIMER'
    text = re.search(patron, data)

    dict_data['modulo'] = text.group(1)
    dict_data['sistema'] = text.group(2)
    dict_data['n_serie'] = text.group(3)

    patron2 = r'PRIMER\s+INGRESO.*?SI.*?(X)?\W+NO.*?(X)?\W+NÚMERO\s+DE\s+SERVICIO\s+ANTERIOR.*?(\d{3,5})'
    text = re.search(patron2, data, flags=re.IGNORECASE)

    if text.group(1):
        dict_data['primer_ingreso'] = "SI"
        dict_data['re_anterior'] = None
    elif text.group(2):
        dict_data['primer_ingreso'] = "NO"
        dict_data['re_anterior'] = text.group(3)

    patron3 = r'OBSERVACIONES:\s*(.*?)\s*RECIBIDO POR:\s*(.+?)\s+(\d{2}/\d{2}/\d{4})'
    text = re.search(patron3, data)
    dict_data['observaciones'] = text.group(1)
    dict_data['recibio'] = text.group(2)
    dict_data['fecha_recibido'] = text.group(3)

    return dict_data

if __name__ == "__main__":
    url_folder_rep = os.path.join(cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_folder"), 
                        cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_notas_rep")
                        )
    
    ruta_pdf = os.path.join(url_folder_rep,
                            r"LS-MR-CT-R-000 Nota de Reparacion RE3167.pdf")
    datos = extraer_tablas_pdf(ruta_pdf)
    data_table = struct_tablas(datos)

    pprint.pprint(data_table)
    datos_solicitante = search_data(data_table['Pag1_Table3'])
    
    pprint.pprint(datos_solicitante)  # Esto imprimirá "LCU"
