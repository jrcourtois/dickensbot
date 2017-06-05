# -*- coding: utf8 -*-
from wikitools.category import Category
import Site
from OrphanPage import OrphanPage
import argparse
import Tools


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
		
print("== Orphelins ==")
print("''Orphelins : %d''" % len(orphan0))
print("{{colonnes|taille=30|")
for p in orphan0:
	print("* [[%s]]" % p)
print("}}")
print("== 1 seul lien ==")
print("''1 seul lien : %d''" % len(orphan1))
print("{{colonnes|taille=30|")
for p in orphan1:
	print("* [[%s]]" % p)
print("}}")
print("== 2 liens ==")
print("''2 liens : %d''" % len(orphan2))
print("{{colonnes|taille=30|")
for p in orphan2:
	print("* [[%s]]" % p)
print("}}")
print("Non orphelins : %d" % (i - len(orphan0) - len(orphan1) - len(orphan2)))



