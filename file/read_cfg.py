import configparser
import os

URL_CONFIG = "config.cfg"
obj_parse = configparser.ConfigParser()
    
def read_config():
    """
    Lectura de archivo .cfg
    """
    try:
        with open(URL_CONFIG, 'r', encoding='utf-8') as configfile:
            obj_parse.read_file(configfile)
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo de configuración: {e}")

def extract_config(file, value):
    """
    Obtiene valor de config
    """
    value = obj_parse[f"{file}"][f"{value}"]

    return value

def update_cfg_url(extension_file, url):
    """
    Actualizo en archivo .cfg url
    """
    obj_parse[f"{extension_file}"]['url'] = url
    
    with open(URL_CONFIG, 'w', encoding='utf-8') as configfile:
        obj_parse.write(configfile)

def update_cfg_url2(url_folder, name_file):
    """
    Actualizo url de archivos solo con ubicacion de carpeta
    """
    url_xlsx = os.join(url_folder, name_file)
    _, extension = os.path.splitext(name_file)
    extension = extension[1:]  # Eliminar el punto inicial
    update_cfg_url(extension, url_xlsx)