from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

#usuario y contraseña para hacer el login
myId = ''
myPin = ''

idPag = str(5831716)
#idPag = str(5831542)

#variable de sitio para login		
site = "http://www.forocoches.com/foro/showthread.php?t=" + idPag

#uso de selenium para hacer el login
browser = webdriver.Chrome("C:/Python/Drivers/chromedriver.exe")
browser.get(site)
browser.find_element_by_name("vb_login_username").send_keys("saposexy");
browser.find_element_by_name("vb_login_password").send_keys("sapo" + Keys.RETURN);

#se vuelve a cargar la url para evitar la peticion de inicio de sesion
browser.get(site)

#obtencion y parseo del codigo html de la pagina
page = browser.find_element_by_tag_name("body").get_attribute("innerHTML");
text = BeautifulSoup(page, "html.parser")

#apertura del fichero csv en el que se va a escribir
ofile = open('usuario-tema(sintratar).csv', 'w', encoding='utf-8-sig')
writer = csv.writer(ofile, delimiter=" ", quotechar='"', lineterminator="\n", quoting=csv.QUOTE_NONE)
writer.writerow(["Usuario"])
writer = csv.writer(ofile, delimiter=" ", quotechar='"', lineterminator="\n", quoting=csv.QUOTE_ALL)

#apertura del fichero csv de temas del que se va a leer
writer.writerow(['nombre'],['idtema'])
rfile = open('temas.csv', 'r', encoding='utf-8-sig')
reader = csv.reader(rfile)

#busqueda de la etiqueta td para encontrar el numero de paginas del hilo
filas = text.find_all("td")
encontradaPag = 0
pag = 1

#para cada uno de los temas en el fichero csv
for tema in reader:
	
	#almacenamos el valor de la columna tema
	numtema = tema[0]
	
	#entra si no es el header del csv
	if numtema != 'id':
	
		print(numtema + ' de ' + reader.count)
		
		#para cada una de las etiquetas td
		for td in filas:
			
			#almacena la clase
			clase = td.get("class")
			
			#comprueba que la clase no sea nula y que el contenido de la etiqueta tampoco
			#luego busca la clase vbmenu_control que controla la paginacion y la palabra
			#Pág en el contenido, ademas de comprobar que no ha almacenado ya el valor
			#necesario, y si no lo almacena
			if clase is not None and td.string is not None:
				if 'vbmenu_control' in clase and 'Pág' in td.string and encontradaPag == 0: 
					encontradaPag = 1
					numPags = td.string[9:]			
		
		#para cada una de las paginas del hilo
		while str(pag) <= numPags:

			#cambia la url por la correspondiente con el id del hilo correspondiente y la pagina
			site = "http://www.forocoches.com/foro/showthread.php?t=" + idPag + "&page=" + str(pag)
			
			#se carga la url con selenium
			browser.get(site)
			
			#obtencion y parseo del codigo html de la pagina
			page = browser.find_element_by_tag_name("body").get_attribute("innerHTML");
			text = BeautifulSoup(page, "html.parser")
			
			#busqueda de la etiqueta a para encontrar a los usuarios en la pagina
			all_links = text.find_all("a")
			
			print(site)
			
			#para cada una de las etiquetas a
			for link in all_links:
			
				#almacena la clase y el href
				href = link.get("href")
				clase = link.get("class")
				
				#comprueba que el href y la clase no sean nulos, y que la cadena 'member' se encuentra
				#en el enlace y que la cadena 'bigusername' se encuentra en la clase, identificando con 
				#esto a los usuarios y escribiendolos en el csv si todo es correcto
				if href is not None and clase is not None:
					if 'member' in href and 'bigusername' in clase: 
						writer.writerow([link.string], [numtema])
			
			#aumentamos la pagina en la que nos encontramos
			pag = pag + 1
		
		#reiniciamos el contador de paginas
		pag = 1
		
#cierra el explorador y los archivos de lectura y escritura
browser.quit()
ofile.close()
rfile.close()		
