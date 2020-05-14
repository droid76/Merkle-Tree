#!/usr/bin/python3
import hashlib,sys
    
class MerkleTreeNode:
    def __init__(self,value):
        self.left = None
        self.right = None
        self.value = value
        self.hashValue = hashlib.sha256(value.encode('utf-8')).hexdigest()
    
def buildTree(leaves,f):
    nodes = []
    for i in leaves:
        nodes.append(MerkleTreeNode(i))

    while len(nodes)!=1:
        temp = []
        for i in range(0,len(nodes),2):
            node1 = nodes[i]
            if i+1 < len(nodes):
                node2 = nodes[i+1]
            else:
                temp.append(nodes[i])
                break
            f.write("Left child : "+ node1.value + " | Hash : " + node1.hashValue +" \n")
            f.write("Right child : "+ node2.value + " | Hash : " + node2.hashValue +" \n")
            concatenatedHash = node1.hashValue + node2.hashValue
            parent = MerkleTreeNode(concatenatedHash)
            parent.left = node1
            parent.right = node2
            f.write("Parent(concatenation of "+ node1.value + " and " + node2.value + ") : " +parent.value + " | Hash : " + parent.hashValue +" \n")
            temp.append(parent)
        nodes = temp 
    return nodes[0]

inputString = sys.argv[1]
leavesString = inputString[1:len(inputString)-1]
leaves = leavesString.split(",")
f = open("merkle.tree", "w")
root = buildTree(leaves,f)
f.close()
    
