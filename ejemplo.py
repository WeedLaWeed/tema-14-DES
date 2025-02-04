import requests
from bs4 import BeautifulSoup

url = "https://es.wikipedia.org/wiki/Wikipedia:Portada"
response=requests.get(url)

soup = BeautifulSoup(response.text,"html.parser")

novedades = soup.find(id='main-cur')

for li in novedades.find_all("li"): 
    print(li.text, end=" "+"\n")