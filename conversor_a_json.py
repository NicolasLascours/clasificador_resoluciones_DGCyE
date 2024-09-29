import re
import json

# Ruta del archivo que contiene el JSON incorrecto
archivo_resoluciones = "resoluciones_modificado.txt"

# Lee el contenido del archivo
with open(archivo_resoluciones, 'r', encoding='utf-8') as archivo:
    contenido = archivo.read()

# Claves que deben ser convertidas a formato JSON
claves_especificas = ["nivel", "origen", "tipo", "numero", "anio", "resumen", "link", "fechasan", "fechaprom", "fechabol", "mfn"]

# Expresión regular para convertir claves específicas a formato JSON
def convertir_a_json(texto):
    # Busca y convierte solo las claves especificadas
    for clave in claves_especificas:
        texto = re.sub(rf'\b{clave}\b:', f'"{clave}":', texto)

    # Quita las comas al final de los objetos JSON (entre } y {)
    texto = texto.replace("},", "},\n")

    # Para asegurar que el último objeto no tenga coma al final
    texto = re.sub(r'},\s*$', '}', texto, flags=re.MULTILINE)
    
    return texto

contenido_json = convertir_a_json(contenido)

resoluciones_salida = "resoluciones.json"
with open(resoluciones_salida, 'w', encoding='utf-8') as archivo_json:
    archivo_json.write(contenido_json)

print(f"Archivo JSON corregido y guardado en {resoluciones_salida}")

