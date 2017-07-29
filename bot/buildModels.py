# -*- coding: utf8 -*-
from USCounty import USCounty
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("state")

templates = open("templates.txt").readlines()
counties = open("counties.txt").readlines()
args = parser.parse_args()

STATE = args.state

i=0
res = []
cError = 0
for t in templates:
	try:
		
		c = USCounty(counties[i].strip(), STATE)
		frenchPalette = c.buildPalette(t.strip())
		c.includePalette()
	except RuntimeError as e:
		print(("Error on %s : %s", (county, e)))
		cError += 1
		if cError > 2:
			break
	except KeyboardInterrupt:
		print("Fin par control C")
		break
	i+=1
