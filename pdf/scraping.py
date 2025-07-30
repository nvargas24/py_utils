import pdfplumber
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from file import read_cfg as cfg
import pprint
import re
import pandas as pd

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

    if flag == "nota":
        patron = r'NOTA\s+DE\s+SERVICIO\s+N°:\s+([A-Z])\s+([A-Z])\s+(\d{3,})'
        text = re.search(patron, data)

        dict_data["tipo_servicio"] = text.group(1)
        dict_data["recibe_loc"] = text.group(2)
        dict_data["num_serv"] = text.group(3)

    elif flag == "solicitante":
        patron = (r'NOMBRE\s+Y\s+APELLIDO:\s*(.*?)\s+SECTOR:\s*(.*?)\s+'    
                 r'Referencia\sIngreso\s-\sO.T.\sN°\s*(.*?)\s+'
                 r'TIPO')

        text = re.search(patron, data)
        dict_data['solicitante'] = text.group(1) if text.group(1) else None
        dict_data['sector_solicitante'] = text.group(2) if text.group(2) else None
        dict_data['ot_num'] = text.group(3) if text.group(3) else None

    elif flag == "tipo":
        patron = (r'DE FORMACIÓN:\s*([xX])?\s+'
                  r'REPARACIÓN DE MÓDULO:\s*([xX])?\s+'
                  r'ENSAYO:\s*([xX])?\sORIGEN'
                  )
        text = re.search(patron, data)

        if text.group(1):
            dict_data['tipo_servicio'] = "Intervención"
        elif text.group(2):
            dict_data['tipo_servicio'] = "Reparación"
        elif text.group(2):
            dict_data['tipo_servicio'] = "Ensayo"

    elif flag == "formacion":
        patron = (r'INTERVENIDA FORMACIÓN\s(.*?)'
                  r'COCHE(.*?)DESCRIPCIÓN'
                  )
        text = re.search(patron, data)

        dict_data['formacion'] = text.group(1)
        dict_data['coche'] = text.group(2)
        
    elif flag == "descripcion":
        patron = r'MODULO\s+(\w+).*?SISTEMA\s+(\w+).*?N° SERIE\s*(\w+)?\s*PRIMER'
        text = re.search(patron, data)

        dict_data['modulo'] = text.group(1)
        dict_data['sistema'] = text.group(2)
        dict_data['n_serie'] = text.group(3)

        patron = r'PRIMER\s+INGRESO.*?SI.*?([xX])?\W+NO.*?([xX])?\W+NÚMERO\s+DE\s+SERVICIO\s+ANTERIOR.*?(\d{3,5})'
        text = re.search(patron, data, flags=re.IGNORECASE)

        if text.group(1):
            dict_data['primer_ingreso'] = "SI"
            dict_data['re_anterior'] = None
        elif text.group(2):
            dict_data['primer_ingreso'] = "NO"
            dict_data['serv_anterior'] = text.group(3)

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
        dict_data['realizado'] = text.group(4)
        dict_data['fecha_reparacion'] = text.group(5)

    elif flag == "verificacion":
        patron = (r'revisión?.*?SI.*?([xX])?\W+NO.*?([xX])?\W+NO.*?'
                  r'PRUEBAS REALIZADAS:\s*-?\s*(.*?)\s*SI.*?'
                  r'UTILIZADOS:\s*-?\s*(.*?)\s*VERIFICADO POR:\s*(.*?)\s*(\d{2}/\d{2}/\d{4})'
                  )

        text = re.search(patron, data)

        if text.group(1):
            dict_data['especificacion_p'] = 'SI'
            dict_data['prueba_realizada'] = text.group(4)
        elif text.group(2):
            dict_data['especificacion_p'] = 'NO'
            dict_data['prueba_realizada'] = text.group(3)

        dict_data['verifico'] = text.group(5)
        dict_data['fecha_verificacion'] = text.group(6)

    return dict_data

def create_dict_data(data_table):
    """
    Extrae datos de pdf y los almacena en un unico diccionario
    """

    nota = search_data(data_table['Pag1_Table2'], "nota")
    solicitante = search_data(data_table['Pag1_Table3'], "solicitante")
    tipo = search_data(data_table['Pag1_Table3'], "tipo")
    formacion = search_data(data_table['Pag1_Table3'], "formacion")
    descripcion = search_data(data_table['Pag1_Table3'], "descripcion")
    trabajos_realizados = search_data(data_table['Pag1_Table4'], "detalle")
    verificacion = search_data(data_table['Pag1_Table5'], "verificacion")

    data_full_pdf = {**nota, **solicitante, **tipo, **formacion,  
                 **descripcion, **trabajos_realizados, **verificacion}
    
    return data_full_pdf

if __name__ == "__main__":
    url_folder_rep = os.path.join(cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_folder"), 
                        cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_notas_rep")
                        )
    
    ruta_pdf = os.path.join(url_folder_rep,
                            r"LS-MR-CT-R-000 Nota de Reparacion RE3199.pdf")
    datos = extraer_tablas_pdf(ruta_pdf) 
    data_table = struct_tablas(datos)
    dict_full_pdf = create_dict_data(data_table)
    df_pdf = pd.DataFrame([dict_full_pdf])

    print(df_pdf)
    print(df_pdf.info())