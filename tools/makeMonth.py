# -*- coding: utf8 -*-
import re
import pprint
from wikitools import api
from wikitools import pagelist
from wikitools import Page
from wikitools import NoPage
from wikitools import Category
from Site import site
from Tools import printProgress
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("month_number")
parser.add_argument("month")
parser.add_argument("year")
args = parser.parse_args()


M = args.month_number.decode("utf8")
m = args.month.decode("utf8")
y = args.year.decode("utf8")


date = '"' + m + " " + y +'"'
month_birth = u"Catégorie:Naissance en " + m + " " + y
month_death = u"Catégorie:Décès en " + m + " " + y

birth_a = []
death_a = []
other_a = []

params = {'action':'query', 'list':'search', 'srsearch':date, 'srlimit' : 50}
request = api.APIRequest(site, params)
result = request.query(False)
snippets = {}
i=0
l = len(result['query']['search'])
for p in result['query']['search']:
	printProgress(i,l)
	i+=1
	page = Page(site,p['title'])
	snippets[p['title']] = re.sub("<.*?>", "", p['snippet'])
	to_add = True
	for c in page.getCategories():
		if c == month_birth:
			birth_a.append(p["title"])
			to_add = False
			continue
		if c == month_death:
			death_a.append(p["title"])
			to_add = False
			continue
	if to_add:
		other_a.append(p["title"])

print "{{Infobox Mois|%s|%s}}" % (M,y)
print
print "== Naissances =="
print u"{{Catégorie détaillée|Naissance en %s %s}}" % (m,y) 
for b in birth_a:
	print "* [[XXXX]] : '''[[%s]]''' (mort le XXX), " % b
	print "<!-- %s -->" % snippets[b]
print
print "== Décès =="
print u"{{Catégorie détaillée|Décès en %s %s}}" % (m,y)
for b in death_a:
	print u"* [[XXXX]] : '''[[%s]]''' (né le XXX), " % b
	print "<!-- %s -->" % snippets[b]
print
print "== Autres événements =="
for b in other_a:
	print "* [[XXX]] : [[%s]]" % b
	print "<!-- %s -->" % snippets[b]
print
print "== Voir aussi =="
print 
print u"{{Portail|années %s}}" % (y[0:3] + "0")


