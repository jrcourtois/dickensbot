# -*- coding: utf8 -*-
from Site import site
from OrphanPage import OrphanPage
from QuickIntersection import QuickIntersection
import Tools
import urllib.error
import datetime

intersec = QuickIntersection(["Portail:Phycologie/Articles liés"])

COUNT = float(intersec.getPageCount())
nbAdopted = 0
nbLinkAdded = 0
nbOrphan = 0
nbError = 0
i = 0
for p in intersec.getPages():
	i += 1
	Tools.printProgress(i, COUNT)
	try:
		page = OrphanPage(p['page_title'])
	except urllib.error.HTTPError:
		print ("Unable to fetch page : %s " % (p['title']))
		nbError += 1
		continue
#	print("%s : %d" % (p['title'], page.getNbLinks()))
	if (page.getNbLinks() > 2):
		nbAdopted += 1
	elif (page.getNbLinks() > 0):
		nbOrphan += 1
	else:

		try:
			nbLinkAdded += Tools.setOrphanIfNeeded(page)
		except:
			print(("Exception occurs: %s" % p['title'] ))
			nbError += 1

print("==== %d orphelins, %d links added, %d adoptés (%d erreurs)" % (nbOrphan, nbLinkAdded, nbAdopted, nbError))

