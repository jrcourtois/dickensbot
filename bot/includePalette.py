# -*- coding: utf8 -*-
import Tools
import re
import time
from lib.ModelPage import ModelPage
import argparse
import pprint

"""
This bot take a Palette and add the palette to all the pages that are referenced in it.
"""

parser = argparse.ArgumentParser()
parser.add_argument("template")
args = parser.parse_args()


t = args.template.decode("utf8")

p = ModelPage(t)
p.parseLinks()



