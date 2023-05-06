# Se debe instalar con pip jinja2 y pdfkit
# Instalar: wkhtmltopdf:
#       en linux:  apt-get install wkhtmltopdf
#       en windows: - descargar e instalar programa de la pag oficial( https://wkhtmltopdf.org/downloads.html)
#                   - se recomienda instalar en una carpeta que no sea el C:
#                   - se debe agregar en PATH (variables de entorno) la carpeta 'bin' de wkhtmltopdf
import jinja2
import pdfkit

def crear_pdf(ruta_template, info, rutacss=''):
    nombre_template = ruta_template.split("/")[-1] # Para obtener ruta de template a partir de la ubicacion
    ruta_template = ruta_template.replace(nombre_template, '')

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(nombre_template)
    html = template.render(info)

    options = { 'page-size': 'Letter',
                'margin-top': '1in',
                'margin-right': '0.5in',
                'margin-bottom': '1in',
                'margin-left': '0.5in',
                'encoding': 'UTF-8'
                }

    config = pdfkit.configuration(wkhtmltopdf='/Users/Homework/Documents/wkhtmltopdf/bin/wkhtmltopdf.exe')
    ruta_salida = '/Users/Homework/Documents/workspace-python/crear_pdf_html/ejemplo.pdf'
    pdfkit.from_string(html, ruta_salida, css=rutacss, options=options, configuration=config)


if __name__ == "__main__":
    ruta_template ='/Users/Homework/Documents/workspace-python/crear_pdf_html/ejemplo.html'
    info = {'nombreAlumno':'Felipe Luna', 'nombreCurso':'Electronica'}
    crear_pdf(ruta_template, info)