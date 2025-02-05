import requests
from bs4 import BeautifulSoup
import mysql.connector
import re  # Para usar expresiones regulares

# URL de la página de fallecimientos en Wikipedia
url = "https://es.wikipedia.org/wiki/Anexo:Fallecidos_en_febrero_de_2025"

# Obtener el HTML de la página
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})  # Simular navegador

# Verificar si la solicitud fue exitosa
if response.status_code != 200:
    print("Error al obtener la página de Wikipedia. Código de estado:", response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Buscar todas las listas de fallecidos (suelen estar en listas <ul><li>)
fallecimientos_section = soup.find_all("ul")

fallecimientos = []

# Extraer información de cada persona fallecida
for lista in fallecimientos_section:
    items = lista.find_all("li")

    for item in items:
        texto = item.text.strip()  # Extraer texto del <li>

        # Extraer el nombre y la edad (si está disponible)
        nombre_edad_match = re.match(r"^(.?)\s\((\d+)\)", texto)
        if nombre_edad_match:
            nombre = nombre_edad_match.group(1).strip()  # Nombre
            edad = int(nombre_edad_match.group(2))       # Edad
        else:
            nombre = texto  # Si no hay edad, usar todo el texto como nombre
            edad = None     # Edad desconocida

        # Limitar el nombre a 255 caracteres
        nombre = nombre[:255]

        # Extraer la fecha de fallecimiento (si está disponible)
        fecha_match = re.search(r"\b(\d{1,2}\sde\s\w+\sde\s\d{4})\b", texto)
        if fecha_match:
            fecha_fallecimiento = fecha_match.group(1)  # Fecha en formato texto
        else:
            fecha_fallecimiento = "2025-02-01"  # Fecha estimada si no se encuentra

        # Guardar los datos en la lista
        fallecimientos.append((nombre, edad, fecha_fallecimiento))

if not fallecimientos:
    print("No se encontraron datos de fallecimientos.")
    exit()

# Conectar con la base de datos MySQL
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia según tu configuración
        password="",  # Si tienes contraseña, ponla aquí
        database="wikipediadb"  # Nombre de la base de datos
    )
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fallecimientos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,  -- Tamaño limitado a 255 caracteres
            edad INT,
            fecha_fallecimiento DATE
        )
    """)

    # Insertar datos en la base de datos
    for fallecido in fallecimientos:
        nombre, edad, fecha_fallecimiento = fallecido

        # Verificar si el nombre ya existe
        cursor.execute("SELECT COUNT(*) FROM fallecimientos WHERE nombre = %s", (nombre,))
        existe = cursor.fetchone()[0]

        if existe == 0:  # Solo insertar si no existe
            cursor.execute("""
                INSERT INTO fallecimientos (nombre, edad, fecha_fallecimiento)
                VALUES (%s, %s, %s)
            """, (nombre, edad, fecha_fallecimiento))

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    cursor.close()
    conn.close()

    print("Datos de fallecimientos guardados en la base de datos sin duplicados.")

except mysql.connector.Error as err:
    print("Error al conectar con la base de datos:", err)