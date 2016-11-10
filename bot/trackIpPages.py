# -*- coding: utf8 -*-
import re
import pprint
from wikitools import api
from wikitools import pagelist
from wikitools import Page
from wikitools import Category
from Site import site
from Tools import printProgress
from Tools import setOrphan
from Tools import isOrphanCat
from OrphanPage import OrphanPage

pageName = u"Projet:Maintenance/Analyse des créations sous IP"
print pageName

p = Page(site,pageName)

print str(len(p.getLinks()))
nbOrphan = 0
toBeAdded = 0

i = 0
lines = p.getLinks()
for l in lines:
	printProgress(i,len(lines))
	i+=1
	p = OrphanPage(l)
	p.setPageInfo()
	if p.pageid < 1:
		print "del"
		continue
	if p.namespace != 0:
		print "not an article"
		continue
	if p.isHomo():
		print "page d'homo"
		continue
	if p.getNbLinks() < 3:
		nbOrphan += 1
		cat = p.getCategories()
		if ( not isOrphanCat(cat)):
			setOrphan(p)
			toBeAdded += 1

print str(nbOrphan) + " among them are orphans"
print str(toBeAdded) + " among them are to be added"
