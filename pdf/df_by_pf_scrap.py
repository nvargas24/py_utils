import pdfplumber
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from file import read_cfg as cfg
from scraping import *
import pprint
import re
import pandas as pd

def pdfs_enable(url_folder):
    """
    Genera una lista con los archivos .pdf en la carpeta solicitada
    """
    pdf_files = []
    patron_pdf = r'^LS-MR-CT-R-000 Nota de Reparación RE\d{4}\.pdf$'

    for archivo in os.listdir(url_folder):
        if archivo.lower().endswith('.pdf'): # verifica pdf
            if re.match(patron_pdf, archivo): # verifica estructura de archivo
                pdf_files.append(archivo)

    return pdf_files

if __name__ == "__main__":
    url_folder_rep = os.path.join(cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_folder"), 
                        cfg.read_config(r"pdf\url_file.cfg", "Reparaciones", "url_notas_rep")
                        )
    
    list_pdfs = pdfs_enable(url_folder_rep)
    pprint.pprint(list_pdfs)
    df_aux = []

    for file_pdf in list_pdfs:
        try:
            ruta_pdf = os.path.join(url_folder_rep, file_pdf)
            datos = extraer_tablas_pdf(ruta_pdf)
            data_table = struct_tablas(datos)
            dict_full_pdf = create_dict_data(data_table)
            df_pdf = pd.DataFrame([dict_full_pdf])
            df_aux.append(df_pdf)
        except Exception as e:
            print(f"Ocurrió un error: {file_pdf} - {e}")

    df = pd.concat(df_aux, ignore_index=True)

    print(df)
    print(df.info())

    