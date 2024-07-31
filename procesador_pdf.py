from PyPDF2 import PdfReader
import re

resolucion = {'fecha':'',
        'numero':'',
        'referencia':'',
        'visto':'',
        'considerando':'',
        'articulos':''        
        }
texto = []
# Abre el archivo PDF
reader = PdfReader("resoluciones/rsc-2020-05906591-gdeba-dgcye.pdf")
for page in reader.pages:
    texto.append(page.extract_text())

texto_unico = ' '.join(texto)

def extraer_seccion(texto, inicio, fin):
    try:
        return re.split(fin, re.split(inicio, texto, maxsplit=1)[1], maxsplit=1)[0].strip()
    except IndexError:
        print(f"Sección '{inicio}' no encontrada o incompleta.")
        return ""

# Extracción de las secciones
resolucion['numero'] = extraer_seccion(texto_unico, 'Número:', 'Referencia')
resolucion['referencia'] = extraer_seccion(texto_unico, 'Referencia:', 'VISTO')
resolucion['visto'] = extraer_seccion(texto_unico, 'VISTO', 'CONSIDERANDO')
resolucion['considerando'] = extraer_seccion(texto_unico, 'CONSIDERANDO', 'Por ello;')
resolucion['articulos'] = extraer_seccion(texto_unico, 'ARTÍCULO 1°', 'archivar.')  

# Impresión de resultados
print("Número:", resolucion['numero'])
print("Referencia:", resolucion['referencia'])
print("VISTO:", resolucion['visto'])
print("CONSIDERANDO:", resolucion['considerando'])
print("ARTÍCULOS:", resolucion['articulos'])

