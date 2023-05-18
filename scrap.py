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

# Ni necesito iniciar sesion xddd
# Configuración de Selenium
driver = webdriver.Chrome("chromedriver.exe")

# # Iniciar sesión con Selenium
# url_login = "https://siiauescolar.siiau.udg.mx"
# driver.get(url_login)

# frame = driver.find_element(By.XPATH, '//frame[@name="mainFrame"]')
# driver.switch_to.frame(frame)

# campo_usuario = driver.find_element(By.XPATH, "//input[@name='p_codigo_c']")
# campo_usuario.send_keys("215662492")

# campo_contraseña = driver.find_element(By.XPATH, "//input[@name='p_clave_c']")
# campo_contraseña.send_keys("chepelone0")

# campo_captcha = driver.find_element(By.ID, 'cpatchaTextBox')
# campo_captcha.send_keys(Keys.RETURN)

# # Esperar a que la página se cargue completamente
# time.sleep(5)

# Web scraping con BeautifulSoup
url = "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta?ciclop="+ciclo+"&crsep=&cup="+centro+"&mostrarp=1000&majrp="+carrera+""
driver.get(url)

updated_html = driver.page_source

# response = requests.get(url)
soup = BeautifulSoup(updated_html, "html.parser")

nrc = []
claveMateria = []
nombreMateria = []
horario = []
dias = []

tbody = soup.find("tbody")

# Obtén los elementos <tr> hijos directos del <tbody>
trs = [tr for tr in tbody.children if tr.name == 'tr']

# Imprime los elementos <tr> encontrados
for tr in trs:
    # Obtén los elementos <td> que son hijos directos del <tr>
    tds = [td for td in tr.children if td.name == 'td']

    # Obtén los datos de los <td> específicos (1, 2, 3 y 8)
    tdsImportantes = [td for i, td in enumerate(tds) if i+1 in [1, 2, 3, 8]]

    # Imprime los datos de los <td> seleccionados
    # for dato in dato:
    #     print(dato)
    
    for idx, td in enumerate(tdsImportantes):
        if(idx == 0):
            nrc.append(td.get_text())
        if(idx == 1):
            claveMateria.append(td.get_text())
        if(idx == 2):
            nombreMateria.append(td.get_text())
        if(idx == 3):
            tdshorario = td.find_all("td")
            if(len(tdshorario) == 0):
                nrc.pop()
                claveMateria.pop()
                nombreMateria.pop()

            tdsImportantesHorario = [tdh for i, tdh in enumerate(tdshorario) if i+1 in [2, 3]]
            for idx2, tdh2 in enumerate(tdsImportantesHorario):
                if(idx2 == 0):
                   horario.append(tdh2.get_text()) 
                if(idx2 == 1):
                   dias.append(tdh2.get_text()) 


# Crear el DataFrame a partir de las listas de columnas
data = {'NRC': nrc, 'Clave Materia': claveMateria, 'Nombre Materia': nombreMateria, 'Horario': horario, 'Dias': dias}
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo Excel
nombre_archivo = 'inco.xlsx'
df.to_excel(nombre_archivo, index=False)

driver.quit()
