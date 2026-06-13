# -*- coding: utf8 -*-
from ModelPage import ModelPage
import argparse
"""
This bot take a Palette and add the palette to all the pages that are referenced in it.
"""

parser = argparse.ArgumentParser()
parser.add_argument("template")
parser.add_argument("--state", default="")
args = parser.parse_args()

t = args.template

p = ModelPage(t)

if (args.state != ""):
    p.parseLinks(["Siège de comté", args.state])
else:
    p.parseLinks()



