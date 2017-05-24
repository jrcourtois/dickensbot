# -*- coding: utf8 -*-
from Site import site
import pprint
from wikitools import api
from OrphanPage import OrphanPage
import Tools


params = {
	'action':'query', 
	'list':'recentchanges', 
	'rctype' : 'new',
	'rcnamespace' : '0', 
	'rcshow' : '!redirect',
	'rclimit':'400'}
r = api.APIRequest(site,params)
result = r.query(False)
nbAdopted = 0
nbLinkAdded = 0
for p in result['query']['recentchanges']:
	
	page = OrphanPage(p['title'])
#	print "%s : %d" % (p['title'], page.getNbLinks())
	Tools.printProgress(nbAdopted + nbLinkAdded, 400)
	if (page.getNbLinks() > 2):
		nbAdopted += 1
	else:
		try:
			nbLinkAdded += Tools.setOrphanIfNeeded(page)
		except:
			print "Exception occurs: %s" % p['title'] 

print "==== %d orphelins, %d adoptés" % (nbLinkAdded, nbAdopted)



