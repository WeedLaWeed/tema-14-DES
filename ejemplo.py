import requests
from bs4 import BeautifulSoup

# URL de la página de actualidad de Wikipedia
url = "https://es.wikipedia.org/wiki/Portal:Actualidad"

# Hacemos la petición a la página
response = requests.get(url)

# Verificamos que la petición fue exitosa (código 200)
if response.status_code == 200:
    # Parseamos el contenido HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Buscamos todos los títulos dentro de los encabezados <h2>, <h3>, etc.
    titulos = soup.find_all(["h2", "h3"])

    print("Títulos de actualidad en Wikipedia:")
    for titulo in titulos:
        print("-", titulo.text.strip())

else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")