# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 13:17:44 2019

@author: marzl
"""
import csv
import random

tsvPaths = [r"C:\Users\marzl\Desktop\telegraphpastopinion.tsv", r"C:\Users\marzl\Desktop\independentpastopinion.tsv"]
outputPath = r"C:\Users\marzl\Desktop\output.tsv"

def randomlyPick30(tsvPath):
    with open(tsvPath, "r", encoding = "utf-8") as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        lineList = ["\t".join(item) for item in tsvreader]
        random.seed()
        return random.choices(lineList, k =30)

randomList = randomlyPick30(tsv1Path) + randomlyPick30(tsv2Path)

with open(outputPath, "w", encoding = "utf-8") as f:
    for item in randomList:
        f.write(str(item) + "\n")
