# -*- coding: utf8 -*-
import re
import pprint
from wikitools import api
from wikitools import pagelist
from wikitools import Page
from wikitools import NoPage
from wikitools import category
from Site import site
from Tools import printProgress
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("day")
parser.add_argument("month")
parser.add_argument("year")
args = parser.parse_args()

d = args.day.decode("utf8")
m = args.month.decode("utf8")
year = args.year.decode("utf8")

date="%s %s %s" % (d,m,year)

month = AlmanachMonth(m, year)
almDay = AlmanachDate(d, m, year)
almDay.parseAndCompare(month)
almDay.printSummary()

p = Page(site, date)
p.edit(text = almDay.getWikiPage().encode("utf8"), summary=u"Créé par un bot, merci de le corriger",bot=True)

#print almDay.getWikiPage()
