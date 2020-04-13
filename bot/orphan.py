# -*- coding: utf8 -*-
import re
from wikitools import api
from wikitools import pagelist
import wikitools
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
	orphan = OrphanPage(p.title)
	if orphan.toAdopt(0):
		print(("%s : already adopted" % p.title))
		continue
	cat = p.getCategories()
	if ( not Tools.isOrphanCat(cat)):
		print((Tools.setOrphan(p)))
		orphans.append(p)
	else:
		print(("%s : tpl already added" % p.title))

print(( "**** " + str(len(orphans)) + " orphans"))

