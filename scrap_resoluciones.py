import requests
import json
import os

# Ruta del archivo JSON
archivo_resoluciones = "resoluciones.json"

# Lee el contenido del archivo
with open(archivo_resoluciones, 'r', encoding='utf-8') as archivo:
    data = json.load(archivo)["data"]

# URL base para descargar los archivos
base_url = "http://catalogo.abc.gov.ar/ServeFileCsj.php?fpath="
directorio_descargas = "resoluciones/"
if not os.path.exists(directorio_descargas):
    os.makedirs(directorio_descargas)
descargas_fallidas = []
def descargar_archivo(resolucion):
    try:
        # Verifica que 'link' esté en la resolución
        if 'link' not in resolucion:
            #print(f"Advertencia: 'link' no encontrado en la resolución: {resolucion}")
            return
        
        url_completa = base_url + resolucion['link']
        nombre_archivo = f"{resolucion['tipo']}_{resolucion['numero']}_{resolucion['anio']}.pdf"        
        ruta_completa_archivo = os.path.join(directorio_descargas, nombre_archivo)
        # Realiza la solicitud HTTP para descargar el archivo
        respuesta = requests.get(url_completa)
        
        if respuesta.status_code == 200:
            # Guarda el archivo en el sistema
            with open(ruta_completa_archivo, 'wb') as file:
                file.write(respuesta.content)
            print(f"Archivo descargado: {ruta_completa_archivo}")
        else:
            descargas_fallidas.append({
                "tipo": resolucion['tipo'],
                "numero": resolucion['numero'],
                "anio": resolucion['anio'],
                "link": resolucion['link'],
                "status_code": respuesta.status_code
            })
            print(f"Error al descargar: {nombre_archivo} (Status Code: {respuesta.status_code})")
    
    except Exception as e:
        # Almacena cualquier excepción como error de descarga
        descargas_fallidas.append({
            "tipo": resolucion['tipo'],
            "numero": resolucion['numero'],
            "anio": resolucion['anio'],
            "link": resolucion['link'],
            "error": str(e)
        })
        print(f"Ocurrió un error al procesar la resolución: {resolucion}. Error: {e}")

# Itera sobre la lista de resoluciones y descarga cada archivo
for resolucion in data:
    descargar_archivo(resolucion)

# Guarda las descargas fallidas en un archivo JSON
salida_fallos = "descargas_fallidas.json"
with open(salida_fallos, 'w', encoding='utf-8') as archivo_json:
    json.dump(descargas_fallidas, archivo_json, indent=4, ensure_ascii=False)

print(f"Descargas fallidas guardadas en {salida_fallos}")
