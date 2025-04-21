import re
import os

# Ruta de la carpeta
carpeta = r"T:\MaterialRodante\Laboratorio\Laboratorio de Electrónica\Reparaciones\Notas de Reparación"

###text = r'(RE) (\d+)'
######text = r"\breparación\b"
text = r"\bRE(\d+)\b"
patron = re.compile(text)

def format_num(match):
    num = int(match.group(1))
    return f'RE{num:04d}'

for archivo in os.listdir(carpeta):
    if patron.search(archivo):
        ###archivo_new = patron.sub(r'\1\2', archivo) # \1 refiere a RE y \2 al num, a ponerlos juntos se borra el espacio
        ######archivo_new = patron.sub("Reparación", archivo)
        archivo_new = patron.sub(format_num, archivo)

        url_old = os.path.join(carpeta, archivo)
        url_new = os.path.join(carpeta, archivo_new)

        os.rename(url_old, url_new)
        print(f'Renombrado: {archivo} a {archivo_new}')
