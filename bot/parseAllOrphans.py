# -*- coding: utf8 -*-
from wikitools.category import Category
from Report import Report
import Site
import time
import pprint

"""
Parse a category and check whether each article is orphan or not.
If it is no more orphan, the template is removed.
Otherwise, we qualify the nature of the file. Does it got translated page, if so, this page is orphan or not ?
Does this translated page have a template on it.

This script does also a report, and put it on the wiki.
"""

start = time.time()
print("Start : " + time.strftime("%H:%M:%S", time.localtime(start) )+ "\n")

report = Report()

i = 0
c = Category(Site.site, "Catégorie:Wikipédia:Tentative d'adoption")
for subCatPage in c.getAllMembersGen():
	a = 0
	subCat = Category(Site.site, subCatPage.title)
	for p in subCat.getAllMembersGen():
		a += 1
		report.parsePage(p.title)
	pprint.pprint( subCatPage.title + ": " + str(a))
	i += a

c = Category(Site.site, "Article orphelin")
for subCatPage in c.getAllMembersGen():
	a = 0
	if subCatPage.title.startswith("Catégorie:Article"):
		subCat = Category(Site.site, subCatPage.title)
		for p in subCat.getAllMembersGen():
			a += 1
			report.parsePage(p.title)
				
		pprint.pprint (subCatPage.title + ": " + str(a))
	i += a


print("Total : " + str(i))


end = time.time()
print("Start : " + time.strftime("%H:%M:%S", time.localtime(start) )+ "\n")
report.printReport()
print(" Fin  du parcours des orphelins : " + time.strftime("%H:%M:%S", time.localtime(end) ) + "\n")

end = time.time()
print("it tooks : " + time.strftime("%H:%M:%S", time.gmtime(end- start)))

