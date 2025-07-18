import pdfplumber

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
                datos.append({
                    "pagina": pagina_num + 1,
                    "tabla": tabla_num + 1,
                    "contenido": tabla_limpia
                })

    return datos

def imprimir_tablas(datos):
    for tabla_info in datos:
        if tabla_info['tabla'] != 1 and \
            tabla_info['tabla'] != 6 and \
            tabla_info['tabla'] != 7 and \
            tabla_info['tabla'] != 8 and \
            tabla_info['tabla'] != 9: 
                print(f"Página: {tabla_info['pagina']} - Tabla: {tabla_info['tabla']}")
                for fila in tabla_info["contenido"]:
                    print(fila)
                print("-" * 40)

if __name__ == "__main__":
    ruta_pdf = r"t:\MaterialRodante\Laboratorio\Laboratorio de Electrónica\Reparaciones\Notas de Reparación\LS-MR-CT-R-000 Nota de Reparación RE3007.pdf"  # Cambia por la ruta de tu PDF
    datos = extraer_tablas_pdf(ruta_pdf)
    imprimir_tablas(datos)