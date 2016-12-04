# -*- coding: utf8 -*-
import re
import pprint
from wikitools import api
from wikitools import pagelist
from wikitools import Page
from wikitools import NoPage
from wikitools import category
from Site import site
from Tools import printProgress
import datetime 
import argparse

MONTH = [u"janvier", u"février", u"mars", u"avril", u"mai", u"juin", u"juillet", u"août", u"septembre", u"octobre", u"novembre", u"décembre"]

WEEK = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

def findBirth(s, date):
	m = re.search(u"n.*? (\d\d? \w+ \d+)", s, re.U)
	if (m):
		if m.group(1) != date :
			return m.group(1)
	m = re.search(u"(\d\d? \w+ \d+).+?(\d\d? \w+ \d+)", s, re.U)
	if (m):
		if m.group(1) != date :
			return m.group(1)
	
	return "XXX"

def findDeath(s, date):
	m = re.search(u"m.*? (\d\d? \w+ \d+)", s, re.U)
	if (m):
		if m.group(1) != date :
			return m.group(1)
	m = re.search(u"(\d\d? \w+ \d+).+?(\d\d? \w+ \d+)", s, re.U)
	if (m):
		if m.group(2) != date :
			return m.group(2)
	return ""
def findOther(s, date):
	m = re.search(u"créé", s, re.U)
	if (m):
		return u"Création"
	m = re.search(u"sort", s, re.U)
	if (m):
		return u"Sortie"
	return False

parser = argparse.ArgumentParser()
parser.add_argument("day")
parser.add_argument("month")
parser.add_argument("year")
args = parser.parse_args()



d = int(args.day.decode("utf8"))
m = args.month.decode("utf8")
year = args.year.decode("utf8")

decade = year[0:3] + "0"
y = int(year)
m_num = MONTH.index(m) + 1

month = "%s %s" % (m, y)
date = "%s %s" % (d, month)
day = datetime.date(y, m_num, d)
dow = WEEK[day.timetuple().tm_wday]
doy = day.timetuple().tm_yday
sdate = '"' + date + '"'
month_birth = u"Catégorie:Naissance en " + month
month_death = u"Catégorie:Décès en " + month

# Récupération des articles liés au mois en question

params = {'action':'query', 'bltitle' : month.title(), 'list':'backlinks','blnamespace':'0', 'blfilterredir':'all', 'bllimit' : 5000}
r = api.APIRequest(site,params)
result = r.query(False)

linkedPage = []

for p in result['query']['backlinks']:
	linkedPage.append(p['title'])

print u"%d pages linked to %s" % (len(linkedPage), month)

cat = category.Category(site,month_birth) 
birth = cat.getAllMembers(True)
print u"%d people born in %s" % (len(birth), month)

cat = category.Category(site,month_death) 
death = cat.getAllMembers(True)
print u"%d people died in %s" % (len(death), month)

params = {'action':'query', 'list':'search', 'srsearch':sdate, 'srlimit' : 1000}
request = api.APIRequest(site, params)
result = request.query(False)

print u"%d pages are concerned with %s" % (len(result['query']['search']), date)

birthArray = {}
deathArray = {}
otherArray = {}
snippets = {}
for p in result['query']['search']:
	snipp = re.sub("<.*?>", "", p['snippet'])
	snippets[p['title']] = snipp
	if p['title'] in birth:
		birthArray[p['title']] = findDeath(snipp, date)
		continue
	if p['title'] in death:
		deathArray[p['title']] = findBirth(snipp, date)
		continue
	if findOther(snipp, date):
		otherArray[p['title']] = findOther(snipp, date)
		continue
	if p['title'] in linkedPage:
		print "==== LINKED ===="
		print p['title']
		print "----"
		print snipp
	else:
		print "==== UNLINKED ===="
		print p['title']
		print "****"
		print snipp

print
print
print "%d people born in %s" % (len(birthArray), date)
print "%d people died in %s" % (len(deathArray), date)
print "%d article linked to %s" % (len(otherArray), date)

ret = u"{{Création automatique|DickensBot}}\n"
ret+= "{{Infobox Jour|%s|%s|%s}}\n" % (d,m_num,y)
ret+= "\n"
ret+= u"Le %s '''%s %s %s''' est le %d{{e}} jour de l'année [[%s]]." % (dow,d,m,y,doy,y)
ret+= "\n"
if len(birthArray) > 0:
	ret+= "\n== Naissances ==\n"
	for b in birthArray:
		if birthArray[b] == "":
			ret+= u"* '''[[%s]]''', \n" % b
		else:
			ret+= u"* '''[[%s]]''' (mort le %s), \n" % (b, birthArray[b])
		ret+= u"<!-- %s -->\n" % snippets[b]
if len(deathArray) > 0:
	ret+= u"\n== Décès ==\n"
	for b in deathArray:
		ret+= u"* '''[[%s]]''' (né le %s), \n" % (b, deathArray[b])
		ret+= u"<!-- %s -->\n" % snippets[b]

ret+= u"\n== Autres événements ==\n"
for b in otherArray:
	ret+= u"* [[%s]] ''(%s)''\n" % (b, otherArray[b])
	ret+= u"<!-- %s -->\n" % snippets[b]

ret+= "\n== Voir aussi ==\n"
ret+= "* [[%s %s]] et [[%s %s]]\n" % (d,m,m,y)
 
ret+= u"\n{{Portail|années %s}}\n" % (decade)

p = Page(site, date)
p.edit(text = ret.encode("utf8"), summary=u"Créé par un bot, merci de le corriger",bot=True)
