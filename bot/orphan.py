# -*- coding: utf8 -*-
import re
from wikitools import api
from wikitools import pagelist
import Site
import Tools
from OrphanPage import OrphanPage

"""
This script parse the orphan pages from Special pages
It add the orphan page template if it is necessary and build the project pages
"""


# define the params for the query
params = {'action':'query', 'list':'querypage', 'qppage':'Lonelypages', 'qplimit':'500', 'qpoffset':'0'}
#params = {'action' : 'query', 'titles':'Main page'}
# create the request object
request = api.APIRequest(Site.site, params)
# query the API
result = request.query(False)

pages = pagelist.listFromQuery(Site.site, result['query']['querypage']['results'])

allCat = {}
orphans = []

for p in pages:
	if p.namespace > 0:
		print p.title + ": not an article"
		continue
	if p.isRedir():
		print p.title + ": redirect"
		continue
	p.setPageInfo()
	if int(p.pageid) < 1:
		print p.title + ": del"
		continue
	orphan = OrphanPage(p.title)
	if orphan.toAdopt():
		print p.title + ": already adopted"
		continue
	cat = p.getCategories()
	if ( not Tools.isOrphanCat(cat)):
		print Tools.setOrphan(p)
		orphans.append(p)
	else:
		print p.title + ": tpl already added"

print( "**** " + str(len(orphans)) + " orphans")

