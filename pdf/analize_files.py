import os
import datetime
import pandas as pd

URL = r"T:\MaterialRodante\Laboratorio\Laboratorio de Electrónica"

registros = []

for root, dirs, files in os.walk(URL):
    for name in files:
        if name.lower().endswith('.pdf'):
            ruta = os.path.join(root, name)
            try:
                fecha_mod = os.path.getmtime(ruta)
                fecha_legible = datetime.datetime.fromtimestamp(fecha_mod)
                registros.append({
                    "archivo": name,
                    "ruta": ruta,
                    "ultima_modificacion": fecha_legible
                })
            except Exception as e:
                print(f"Error con el archivo: {ruta}\n{e}")

df = pd.DataFrame(registros)
df['hipervinculo'] = df['ruta'].apply(lambda x: f'=HYPERLINK("{x}", "Abrir archivo")')

print(df)
print(df.info())

df.to_excel('indice de archivos.xlsx', index=False, sheet_name='PDF')