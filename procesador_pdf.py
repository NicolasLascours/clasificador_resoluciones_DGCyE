from PyPDF2 import PdfReader
import re, csv, os

resolucion = {'fecha':'',
        'numero':'',
        'referencia':'',
        'visto':'',
        'considerando':'',
        'articulos':''        
        }
texto = []
# Abre el archivo PDF
reader = PdfReader("resoluciones/EX–2022-42817554-GDEBA-SDCADDGCYE - Calendario Escolar 2023.pdf")
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

csv_filename = 'resoluciones.csv'
file_exists = os.path.exists(csv_filename)
# Escribir los datos en un archivo CSV
with open(csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['fecha', 'numero', 'referencia', 'visto', 'considerando', 'articulos']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

    # Escribir el encabezado solo si el archivo no existía previamente
    if not file_exists:
        writer.writeheader()
    
    # Escribir los datos de la nueva resolución
    writer.writerow(resolucion)

