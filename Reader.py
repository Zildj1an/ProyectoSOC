import csv

ofile = open('origen.csv', 'r', encoding='utf-8-sig')
reader = csv.reader(ofile)

wfile = open('temas.csv', 'r', encoding='utf-8-sig')
writer = csv.writer(wfile, delimiter='', quotechar='"', quoting=csv.QUOTE_NONE)

rownum = 0

for row in reader:
	if rownum == 0:
		writer.writerow(['id'], ['tema'])
	else 
		writer.writerow([str(rownum)], [row[1]])	
	rownum += 1
	
ofile.close
wfile.close