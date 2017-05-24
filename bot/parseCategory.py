# -*- coding: utf8 -*-
from wikitools import Category
from lib import Site
from OrphanPage import OrphanPage
import argparse
from lib import Tools


parser = argparse.ArgumentParser("To parse a category")
parser.add_argument("catName")
args = parser.parse_args()
catName = args.catName.decode("utf8")

cat = Category(Site.site,catName) 

tab = cat.getAllMembers(True)

pages = {}
orphan0 = []
orphan1 = []
orphan2 = []

i = 0
for p in tab:
	i+=1
#	Tools.printProgress(i, len(tab))
	page = OrphanPage(p)
	if page.getNbLinks()==0:
		orphan0.append(p)
	if page.getNbLinks()==1:
		orphan1.append(p)
	if page.getNbLinks()==2:
		orphan2.append(p)
		
print "Orphelins : %d" % len(orphan0)
for p in orphan0:
	print "[[%s]]" % p.title()
print "1 seul lien : %d" % len(orphan1)
for p in orphan1:
	print "[[%s]]" % p.title()
print "2 liens : %d" % len(orphan2)
for p in orphan2:
	print "[[%s]]" % p.title()
print "Non orphelins : %d" % (i - len(orphan0) - len(orphan1) - len(orphan2))



