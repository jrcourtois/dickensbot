# -*- coding: utf8 -*-
from USCounty import USCounty
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("englishTemplate")
parser.add_argument("county")
parser.add_argument("state")
parser.add_argument("--noPrint", action='store_true', dest='noPrint')
parser.add_argument("--noEdit", action='store_true', dest='noEdit')
args = parser.parse_args()

t = args.englishTemplate
county = args.county
state = args.state

try:
	c = USCounty(county, state)
	frenchPalette = c.buildPalette(t)
	c.include()
except RuntimeError as e:
	print(("Error on %s : %s", (county, e)))
	cError += 1
