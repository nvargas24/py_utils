import configparser
import os

obj_parse = configparser.ConfigParser()
    
def read_config(url_cfg, key, param):
    """
    Lectura de archivo .cfg
    :param key: clave de config. en []
    :param param: tipo de config. 
    :return value: extraccion
    """
    
    obj_parse = configparser.ConfigParser()
    try:
        with open(url_cfg, 'r', encoding='utf-8') as configfile:
            obj_parse.read_file(configfile)
            value = obj_parse[f"{key}"][f"{param}"].strip('"')
    except Exception as e:
        raise RuntimeError(f"Error al leer el archivo de configuración: {e}")
    
    return value

def update_param(url_cfg, key, param, new_value):
    """
    Actualizo parametro en archivo cfg
    """
    obj_parse = configparser.ConfigParser()
    obj_parse[f"{key}"][f"{param}"] = new_value
    
    with open(url_cfg, 'w', encoding='utf-8') as configfile:
        obj_parse.write(configfile)

def update_cfg_url(url_cfg, url_folder, name_file):
    """
    Actualizo url de archivos solo con ubicacion de carpeta
    """
    url_xlsx = os.join(url_folder, name_file)
    _, extension = os.path.splitext(name_file)
    extension = extension[1:]  # Eliminar el punto inicial
    update_cfg_url(url_cfg, extension, 'url', url_xlsx)