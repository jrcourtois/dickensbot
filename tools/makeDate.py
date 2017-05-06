# -*- coding: utf8 -*-

import argparse

from WikiDate import WikiDate
from wikitools import Page
from Site import site


parser = argparse.ArgumentParser()
parser.add_argument("day")
parser.add_argument("month")
parser.add_argument("year")
args = parser.parse_args()

d = args.day.decode("utf8")
m = args.month.decode("utf8")
year = args.year.decode("utf8")

almDay = WikiDate(int(d), int(m), int(year))

print almDay.getWikiPage()

p = Page(site, almDay.date)

p.edit(text = almDay.getWikiPage().encode("utf8"), summary=u"Créé par un bot, merci de le corriger",bot=True)
