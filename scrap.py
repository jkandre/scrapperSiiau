import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

ciclo = "202310"
centro = "D"
carrera = "INCO"

# Configuración de Selenium
driver = webdriver.Chrome("chromedriver.exe")

# Iniciar sesión con Selenium
url_login = "https://siiauescolar.siiau.udg.mx"
driver.get(url_login)

frame = driver.find_element(By.XPATH, '//frame[@name="mainFrame"]')
driver.switch_to.frame(frame)

campo_usuario = driver.find_element(By.XPATH, "//input[@name='p_codigo_c']")
campo_usuario.send_keys("215662492")

campo_contraseña = driver.find_element(By.XPATH, "//input[@name='p_clave_c']")
campo_contraseña.send_keys("chepelone0")

campo_captcha = driver.find_element(By.ID, 'cpatchaTextBox')
campo_captcha.send_keys(Keys.RETURN)

# Esperar a que la página se cargue completamente
time.sleep(5)

# Web scraping con BeautifulSoup
url = "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop="+ciclo+"&crsep=&cup="+centro+"&mostrarp=1000&majrp="+carrera+""
driver.get(url)

updated_html = driver.page_source

soup = BeautifulSoup(updated_html, "html.parser")

titulos = []
tbody = soup.find("tbody")

# Obtén los elementos <tr> hijos directos del <tbody>
trs = [tr for tr in tbody.children if tr.name == 'tr']

# Imprime los elementos <tr> encontrados
for tr in trs:
    print(tr.prettify())

# for enlace in enlaces:
#     titulo = enlace.get("title")
#     if titulo:
#         titulos.append(titulo)

# df = pd.DataFrame(titulos, columns=["Título"])
# df.to_excel("titulos_wikipedia.xlsx", index=False)

# Cerrar el controlador de Selenium
driver.quit()
