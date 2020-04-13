# -*- coding: utf8 -*-
from USCounty import USCounty
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("state")
parser.add_argument("--includeOnly", action='store_true', dest='includeOnly')

templates = open("templates.txt").readlines()
counties = open("counties.txt").readlines()
args = parser.parse_args()

STATE = args.state

i=0
res = []
cError = 0
if args.includeOnly == False:
	for t in templates:
		try:
			c = USCounty(counties[i].strip(), STATE)
			frenchPalette = c.buildPalette(t.strip())
		except RuntimeError as e:
			print(("Error on %s : %s", (t, e)))
			cError += 1
			if cError > 2:
				break
		except KeyboardInterrupt:
			print("Fin par control C")
			quit()
		i+=1


for county in counties:
	try:
		c = USCounty(county.strip(), STATE)
		c.includePalette()
	except RuntimeError as e:
		print(("Error on %s : %s", (county, e)))
		cError += 1
		if cError > 2:
			break
	except KeyboardInterrupt:
		print("Fin par control C")
		break
