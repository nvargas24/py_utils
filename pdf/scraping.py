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

def search_data(data, flag):
    dict_data = {}
    # Descripcion del componente o sistema a reparar, revisar o ensayar
    if flag == "descripcion":
        patron = r'MODULO\s+(\w+).*?SISTEMA\s+(\w+).*?N° SERIE\s*(\w+)?\s*PRIMER'
        text = re.search(patron, data)

        dict_data['modulo'] = text.group(1)
        dict_data['sistema'] = text.group(2)
        dict_data['n_serie'] = text.group(3)

        patron = r'PRIMER\s+INGRESO.*?SI.*?(X)?\W+NO.*?(X)?\W+NÚMERO\s+DE\s+SERVICIO\s+ANTERIOR.*?(\d{3,5})'
        text = re.search(patron, data, flags=re.IGNORECASE)

        if text.group(1):
            dict_data['primer_ingreso'] = "SI"
            dict_data['re_anterior'] = None
        elif text.group(2):
            dict_data['primer_ingreso'] = "NO"
            dict_data['re_anterior'] = text.group(3)

        patron = r'OBSERVACIONES:\s*(.*?)\s*RECIBIDO POR:\s*(.+?)\s+(\d{2}/\d{2}/\d{4})'
        text = re.search(patron, data)
        dict_data['observaciones'] = text.group(1)
        dict_data['recibio'] = text.group(2)
        dict_data['fecha_recibido'] = text.group(3)
    
    elif flag == "detalle":
        # Descripcion de los trabajos realizados
        patron = (
                r'NOMBRE OPERARIO DE TALLER \(Solo Intervenciones o ensayos\)\s*'
                r'(.*?)\s*'
                r'DETALLE DE LOS TRABAJOS REALIZADOS:\s*(.*?)\s*'
                r'MATERIALES UTILIZADOS:\s*(.*?)\s*'
                r'REALIZADO POR:\s*(.*?)\s*(\d{2}/\d{2}/\d{4})'
                  )

        text = re.search(patron, data)

        dict_data['operario_taller'] = text.group(1) if text.group(1) else None
        dict_data['detalle_trabajos'] = text.group(2)
        dict_data['materiales'] = text.group(3)
        dict_data['realializo'] = text.group(4)
        dict_data['fecha_reparacion'] = text.group(5)

    return dict_data

if __name__ == "__main__":
    url_folder_rep = os.path.join(cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_folder"), 
                        cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_notas_rep")
                        )
    
    ruta_pdf = os.path.join(url_folder_rep,
                            r"LS-MR-CT-R-000 Nota de Reparacion RE3175.pdf")
    datos = extraer_tablas_pdf(ruta_pdf)
    
    data_table = struct_tablas(datos)
    pprint.pprint(data_table)

    descripcion = search_data(data_table['Pag1_Table3'], "descripcion")
    pprint.pprint(descripcion)

    trabajos_realizados = search_data(data_table['Pag1_Table4'], "detalle")
    pprint.pprint(trabajos_realizados)
