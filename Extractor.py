from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import csv

ofile = open('prueba.csv', 'w', encoding='utf-8-sig')
writer = csv.writer(ofile, delimiter=" ", quotechar='"', lineterminator="\n", quoting=csv.QUOTE_NONE)
writer.writerow(["Usuario"])
writer = csv.writer(ofile, delimiter=" ", quotechar='"', lineterminator="\n", quoting=csv.QUOTE_ALL)

myId = '<your_id_here>'
myPin = '<your_pin_here>'
data = {
            'id':myId,
            'PIN':myPin,
            'submit':'Request Access',
            'wcuirs_uri':''
        }
		
binaryData = urlencode(data).encode('UTF-8')
		
site = "http://www.forocoches.com/foro/showthread.php?t=5831542"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req, binaryData)
text = BeautifulSoup(page, "html.parser")

filas = text.find_all("td")

encontradaPag = 0
pag = 1

for td in filas:
	clase = td.get("class")
	
	if clase is not None and td.string is not None:
		if 'vbmenu_control' in clase and 'Pág' in td.string and encontradaPag == 0: 
			encontradaPag = 1
			numPags = td.string[9:]			
			
while str(pag) <= numPags:

	site = "http://www.forocoches.com/foro/showthread.php?t=5831542&page=" + str(pag)
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(site,headers=hdr)
	page = urlopen(req, binaryData)
	text = BeautifulSoup(page, "html.parser")

	all_links = text.find_all("a")

	pag = pag + 1
	print(site)
	for link in all_links:
		href = link.get("href")
		clase = link.get("class")
		if href is not None and clase is not None:
			if 'member' in href and 'bigusername' in clase: 
				writer.writerow([link.string])