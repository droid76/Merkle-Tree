#!/usr/bin/python3
import hashlib,sys
    
class MerkleTreeNode:
    def __init__(self,value):
        self.left = None
        self.right = None
        self.value = value
        self.hashValue = getHashValue(value)
    
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

def getHashValue(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def combined(value1,value2):
    combinedValue = value1+value2
    return combinedValue


def checkConsistency(leaves1,leaves2):
    i=0
    while i<len(leaves1):
        if leaves1[i]!=leaves2[i]:
            break
        i+=1
    if i < len(leaves1):
        return []
    f = open("merkle.trees", "w")
    f.write("Merkle Tree 1 \n")
    root1 = buildTree(leaves1,f)
    f.write("\n\n")
    f.write("Merkle Tree 2 \n")
    root2 = buildTree(leaves2,f)
    f.close()
    op = []
    op.append(root1.hashValue)
    with open("merkle.trees") as f:
        data = f.readlines()
    
    tree2Index = 0
    for i in range(len(data)):
        if data[i].startswith("Merkle Tree 2"):
            tree2Index = i
    parentLines = []
    leftChildLines = []
    rightChildLines = []
    for i in range(tree2Index,len(data)):
        if data[i].startswith("Parent("):
            parentLines.append(data[i])
    
    for i in range(tree2Index,len(data)):
        if data[i].startswith("Left"):
            leftChildLines.append(data[i])

    for i in range(tree2Index,len(data)):
        if data[i].startswith("Right"):
            rightChildLines.append(data[i])  
    op = []
    flag = False
    for i in range(len(parentLines)):
        if root1.hashValue in parentLines[i]:
            flag = True
            break
    if flag:
        values = []    
        combinedHash = ''
        lc = root1.value
        while combinedHash != root2.hashValue:
            for i in range(len(leftChildLines)):
                if lc in leftChildLines[i].split(" ")[-6]:
                    rc = rightChildLines[i].split(" ")[-6]
                    values.append(getHashValue(rc))
                    break
            combinedValue = combined(getHashValue(lc),getHashValue(rc))
            combinedHash = getHashValue(combinedValue)
            lc = combinedValue
            
        op.append(root1.hashValue)
        op+=values
        op.append(root2.hashValue)
                
    else:
        root1LeftChildValue = data[tree2Index-5].split(" ")[-6]
        root1RightChildValue = data[tree2Index-4].split(" ")[-6]
        root1RightChildSiblingValue = leaves2[leaves2.index(root1RightChildValue)+1]
        values = []
        values.append(getHashValue(root1LeftChildValue))
        values.append(getHashValue(root1RightChildValue))
        values.append(getHashValue(root1RightChildSiblingValue))
        root1RightChildCombinedValue = combined(getHashValue(root1RightChildValue),getHashValue(root1RightChildSiblingValue))        
        combinedHash = ''
        lc = root1LeftChildValue
        rc = root1RightChildCombinedValue
        while combinedHash != root2.hashValue:
            combinedValue = combined(getHashValue(lc),getHashValue(rc))
            combinedHash = getHashValue(combinedValue)
            lc = combinedValue
            for i in range(len(leftChildLines)):
                if lc in leftChildLines[i].split(" ")[-6]:
                    rc = rightChildLines[i].split(" ")[-6]
                    values.append(getHashValue(rc))
                    break
            
        op.append(root1.hashValue)
        op+=values
        op.append(root2.hashValue)
                
    return op

inputString1 = sys.argv[1]
inputString2 = sys.argv[2]
leavesString1 = inputString1[1:len(inputString1)-1]
leaves1 = leavesString1.split(",")
leavesString2 = inputString2[1:len(inputString2)-1]
leaves2 = leavesString2.split(",")

op = checkConsistency(leaves1,leaves2)
if len(op) > 0:
    print("Yes",op)
else:
    print("No")


    
