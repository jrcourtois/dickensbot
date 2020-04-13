# -*- coding: utf8 -*-

import argparse

from WikiMonth import WikiMonth
from wikitools.page import Page
from Site import site


parser = argparse.ArgumentParser()
parser.add_argument("month")
parser.add_argument("year")
args = parser.parse_args()

m = args.month
year = args.year

almMonth = WikiMonth(int(m), int(year))

print(almMonth.getWikiPage())

p = Page(site, almMonth.date)


p.edit(text = almMonth.getWikiPage(), summary="Créé par un bot, merci de le corriger",bot=True)
