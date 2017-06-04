# -*- coding: utf8 -*-

from wikitools import Page
from Site import site
from AlmanachDate import AlmanachDate, AlmanachMonth
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("month")
parser.add_argument("year")
args = parser.parse_args()

m = args.month.decode("utf8")
year = args.year.decode("utf8")

month = AlmanachMonth(m, year)
monthArray = []
aDay = AlmanachDate("1er", m, year)		
monthArray.append(aDay)
aDay.parseAndCompare(month)
aDay.printSummary()

for i in range(2,32):
	try:
		aDay = AlmanachDate(i, m, year)		
		monthArray.append(aDay)
		aDay.parseAndCompare(month)
		aDay.printSummary()
	except:
		print(("No %s %s %s" % (i, m, year)))

		
ret = "{{Création automatique|DickensBot}}\n"
ret+= "{{Infobox Mois|%s|%s}}\n" % (month.getNum(),year)
ret+= "\n== Naissances ==\n"
ret+= "{{Catégorie détaillée|Naissance en %s %s}}\n" % (m,year) 
for d in monthArray:
	if len(d.birthArray) > 0:
		ret+= "'''[[%s %s]]'''\n" % (d.d, m)
		ret+= d.getBirths()
ret+= "\n== Décès ==\n"
ret+= "{{Catégorie détaillée|Décès en %s %s}}\n" % (m,year) 
for d in monthArray:
	if len(d.deathArray) > 0:
		ret+= "'''[[%s %s]]'''\n" % (d.d, m)
		ret+= d.getDeaths()
ret+= "\n== Evènements ==\n"
for d in monthArray:
	if d.hasOther() > 0:
		ret+= "'''[[%s %s]]'''\n" % (d.d, m)
		ret+= d.getAll()

ret+= "\n== Voir aussi ==\n"
ret+= "\n{{Portail|années %s}}" % (year[0:3] + "0")

date = "%s %s" % (m, year)

p = Page(site, date)
p.edit(text = ret, summary="Créé par un bot, merci de compléter", bot=True)
