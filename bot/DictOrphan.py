# -*- coding: utf8 -*-
import re
from wikitools import api
from wikitools import pagelist
import wikitools
import Site
import Tools
from wikitools.page import Page
from wikitools.category import Category

cat = Category(Site.wikt,"Langues") 

allLanguages = cat.getAllMembers(True)

print(len(allLanguages))

"""
This script parse the orphan pages from Special pages
It add the orphan page template if it is necessary and build the project pages
"""


def getList(offset):
	# define the params for the query
	params = {'action':'query', 'list':'querypage', 'qppage':'Lonelypages', 'qplimit':'500', 'qpoffset':offset}
	#params = {'action' : 'query', 'titles':'Main page'}
	# create the request object
	request = api.APIRequest(Site.wikt, params)
	# query the API
	result = request.query(False)

	return pagelist.listFromQuery(Site.wikt, result['query']['querypage']['results'])

pages = []
for i in ['0', '500', '1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500']:
	pages += getList(i)
	print (i)

allCat = {}
orphans = []

time = 0
COUNT = len(pages)
for p in pages:
	Tools.printProgress(time, COUNT)
	time += 1
	if p.namespace > 0:
		print(("%s : not an article" % p.title))
		continue
	try:
		if p.isRedir():
			print(("%s : redirect" % p.title))
			continue
	except wikitools.exceptions.NoPage:
		print ("%s: not found" % p.title)
		continue
	p.setPageInfo()
	if int(p.pageid) < 1:
		print(("%s : del" % p.title))
		continue
	cat = p.getCategories()

	if 'Catégorie:Noms de famille en français' in cat:
		orphans.append(p.title)
	else:
		for c in cat:
			if not c in allCat:
				allCat[c] = []
			allCat[c].append(p.title)


t = "== Noms de famille en français ==\n{{colonnes|taille=30|\n"
for orphan in orphans:
	t += "* [[%s]]\n" % (orphan)
t += "}}\n"

t += "== Autres catégories ==\n"
other = "== Reste ==\n{{colonnes|taille=30|\n"

for c in allCat:
	if c in allLanguages:
		t += "=== [[:%s]] ===\n{{colonnes|taille=30|\n" % (c)
		for orphan in allCat[c]:
			t += "* [[%s]]\n" % (orphan)
		t += "}}\n"
	else:
		if len(allCat[c]) > 50:
			other += "* [[:%s]] : %d\n" % (c, len(allCat[c]))

t += other + "}}\n"

orphPage =  Page(Site.wikt,"Projet:Pages orphelines/Liste de pages")
orphPage.edit(text=t,bot=True, summary="Création")

