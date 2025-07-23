import pdfplumber
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from file import read_cfg as cfg
import pprint

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
                str_table = ' '.join(' '.join(map(str, fila)) for fila in tabla_limpia)
                
                datos.append({
                    "pagina": pagina_num + 1,
                    "tabla": tabla_num + 1,
                    "contenido": str_table
                })

    return datos

def struct_tablas(datos):
    tablas = {}

    for tabla_info in datos:
        tablas[f"Pag{tabla_info['pagina']}_Table{tabla_info['tabla']}"] = tabla_info['contenido']

    return tablas

if __name__ == "__main__":
    url_folder_rep = os.path.join(cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_folder"), 
                        cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_notas_rep")
                        )
    
    ruta_pdf = os.path.join(url_folder_rep,
                            r"LS-MR-CT-R-000 Nota de Reparación RE3007.pdf")
    datos = extraer_tablas_pdf(ruta_pdf)
    data_table = struct_tablas(datos)

    pprint.pprint(data_table)