# -*- coding: utf8 -*-
from Site import site
import pprint
from wikitools import api
from OrphanPage import OrphanPage
import Tools

COUNT = 400

params = {
	'action':'query', 
	'list':'recentchanges', 
	'rctype' : 'new',
	'rcnamespace' : '0', 
	'rcshow' : '!redirect',
	'rclimit': COUNT}

r = api.APIRequest(site, params)
result = r.query(False)
nbAdopted = 0
nbLinkAdded = 0
nbOrphan = 0
nbError = 0
i = 0
for p in result['query']['recentchanges']:
	i += 1
	Tools.printProgress(i, COUNT)
	try:
		page = OrphanPage(p['title'])
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
			nbError += 1z

print("==== %d orphelins, %d links added, %d adoptés (%d erreurs)" % (nbOrphan, nbLinkAdded, nbAdopted, nbError))

