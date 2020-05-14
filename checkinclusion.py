#!/usr/bin/python3
import ast,sys,hashlib

def parseFile():
    f = open("merkle.tree","r")
    tree ={}
    for line in f:
        lineArray = line.split(" ")
        if lineArray[0] == 'Parent(concatenation':
            tree[lineArray[6]] = lineArray[10]
        else:
            tree[lineArray[3]] = lineArray[7]
    return tree

def checkInclusion(inputString,tree):
    op = []
    for key,value in tree.items():
        if inputString in key:
            op.append(value)
            inputString = value
    return op

inputString = sys.argv[1]
tree = parseFile()
op = checkInclusion(inputString,tree)
if(len(op)> 0):
    print("yes",op)
else:
    print("no")