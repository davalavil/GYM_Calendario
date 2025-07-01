import os
import json
from datetime import datetime

# --- CONFIGURACIÓN ---
VIDEO_FOLDER = 'Videos'  # La carpeta donde están tus videos
OUTPUT_FILE = 'video_data.json' # El archivo JSON que se generará
BASE_URL = 'Videos/' # La ruta base para acceder a los videos desde el HTML

def extract_video_info(filename):
    """
    Extrae la fecha y el nombre legible del archivo de video.
    Formato esperado: XXYYDD_Nombre_Legible.extension
    """
    # Validar formato inicial (6 dígitos seguidos de '_')
    if len(filename) < 11 or not filename[:6].isdigit() or filename[6] != '_':
        # Ignorar archivos que no cumplen el formato esperado
        return None

    date_str = filename[:6]
    try:
        # Asumimos que los años son del siglo XXI (añadimos '20')
        year = int("20" + date_str[:2])
        month = int(date_str[2:4])
        day = int(date_str[4:6])
        video_date = datetime(year, month, day)
    except ValueError:
        # Error al parsear la fecha si los dígitos no forman una fecha válida
        return None

    # Obtener el nombre del archivo sin la extensión
    name_without_ext, _ = os.path.splitext(filename)
    
    # El nombre legible es todo lo que viene después de 'XXYYDD_'
    # Si el nombre_sin_ext tiene al menos 7 caracteres (XXYYDD_), extraemos a partir del 7º
    if len(name_without_ext) > 7:
        readable_name = name_without_ext[7:] 
    else:
        # Si no hay nombre legible después de la fecha, usamos el nombre original (sin extensión)
        readable_name = name_without_ext 

    return {
        "date": video_date.strftime('%Y-%m-%d'), # Formato para clave del calendario
        "readable_name": readable_name,
        "url": BASE_URL + filename # Ruta para el enlace HTML
    }

def generate_json_data():
    """
    Escanea la carpeta de videos y genera el archivo JSON.
    """
    video_data = {} # Usaremos un diccionario donde la clave es la fecha

    if not os.path.isdir(VIDEO_FOLDER):
        print(f"Error: La carpeta '{VIDEO_FOLDER}' no existe. Asegúrate de que esté en el mismo directorio que el script.")
        return

    # Lista de extensiones de video comunes
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm')

    for filename in os.listdir(VIDEO_FOLDER):
        # Comprobar si el archivo tiene una extensión de video y coincide con el formato esperado
        if filename.lower().endswith(video_extensions):
            info = extract_video_info(filename)
            if info:
                date_key = info["date"]
                if date_key not in video_data:
                    video_data[date_key] = []
                video_data[date_key].append({
                    "readable_name": info["readable_name"],
                    "url": info["url"]
                })

    # Guardar los datos en un archivo JSON
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # Usamos ensure_ascii=False para permitir caracteres especiales y indent=4 para una buena lectura
            json.dump(video_data, f, ensure_ascii=False, indent=4)
        print(f"¡Éxito! Datos de video generados y guardados en '{OUTPUT_FILE}'")
        print(f"Ahora puedes servir tu proyecto con un servidor web (ej: 'python -m http.server') y abrir 'http://localhost:8000' en tu navegador.")
    except IOError as e:
        print(f"Error al escribir el archivo '{OUTPUT_FILE}': {e}")

if __name__ == "__main__":
    generate_json_data()