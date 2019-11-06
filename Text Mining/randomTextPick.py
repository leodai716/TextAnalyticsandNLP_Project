# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 13:17:44 2019

@author: marzl
modified by: leod
"""
import csv
import random
import sys

sys.path.append("../")

import _LocalVariable

tsvPaths = _LocalVariable._DATA_DIRECTORY + r"\raw_data-opinion-gardian.tsv"
outputPath = _LocalVariable._DATA_DIRECTORY + r"\raw_data-BrexitorNot-opinion.tsv"

def randomlyPick60(tsvPath):
    with open(tsvPath, "r", encoding = "utf-8") as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        lineList = ["\t".join(item) for item in tsvreader]
        random.seed()
        return random.choices(lineList, k =60)

randomList = randomlyPick60(tsvPaths)

with open(outputPath, "w", encoding = "utf-8") as f:
    for item in randomList:
        f.write(str(item) + "\n")
