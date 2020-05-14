# Description
There are three Python programs in this repo:

### buildmtree.py
Creates a merkle tree and writes the tree output into a file "merkle.tree" to represent in a user friendly format. 
The program contains the following components:
   1. Input to program: The program reads the list input to the program as a string, extracts all the strings and then appends into a         list. This will contain all our leaf nodes
   2. A MerkleTreeNode class: This is used to create a merkle tree node and has 4 properties:
      1. Left child of the node
      2. Right child of the node
      3. Value of the node
      4. Hashvalue of the node. The sha256 function of the hashlib library is used to compute all the hash values
   3. The buildTree function: This takes the list of leaf nodes and the file object as input. A binary tree is constructed in a top down       manner accounting for both odd and even number of leaf nodes and in every iteration the left child value and hash, the right             child value and hash and the parent value and hash of the children is written to the file.

Screenshots:
![buildmtree screenshot](https://github.com/droid76/Merkle-Tree/blob/master/Screenshots/buildmtree.png)
Explanation of merkle.tree output format:
The left child value of the node and its hash is first printed, the next line prints the value of the node and its hash and finally      the value of the parent and its hash is printed. Some of the node values may appear to be large. This is because these values are        formed by concatenating the hashes of the children.

### checkinclusion.py
This program takes a certain string as input and returns whether the string exists in the merkle tree constructed by the         buildmtree.py program and the hashes of the intermediate nodes used to verify the output
The program contains the following components:
   1.  parseFile function: This reads the merkle.tree file and creates a dictionary representing the tree where the key is the value of        the node and the value is the hash of that node
   2.  checkInclusion function: This takes the dictionary constructed in the parseFile function and the input string and while                  traversing through the dictionary, checks if the inputstring is a key in the dictionary. If it exists, that means that the string        is present in the merkle tree and its value corresponds to the hash of the node used to check for the proof. The value is then          added to the output list and input string now becomes this hash. Next this new input string is then checked in the dictionary and        if present, the corresponding hash is added to the output list and the input string becomes this hash. In this way we get the            intermediate nodes. The output list is then finally returned at the end of the function
At the end of both functions if output list is empty, that means that the string does not exist in the tree and the string "No" is printed. Else, the string "Yes" is printed, and the output list is printed.

Screenshots:

If the input to buildmtree.py was [alice,bob,carol,david,eve]:
![checkinclusion screenshot](https://github.com/droid76/Merkle-Tree/blob/master/Screenshots/checkinclusion.png)
Here, the strings "bob" and "eve" exist in the tree and so the string “yes” along with their proofs are printed. Strings "richard" and "alex" don’t exist in the tree and so just the string "no" is printed.

### checkconsistency.py
This program takes two lists of nodes as input, verifies that they are consistent and outputs the consistency proof. **Assumption: First list is always smaller than second list**
The program consists of the following components:
   1. MerkleTreeNode class and buildTree function: These are taken from the buildmtree.py file and are used to construct both the trees       and output them onto the merkle.trees file.
   2. checkconsistency function: This function first checks if the first list is an exact subset of the second list. If no, then the           output list remains empty. If yes, we move on to the consistency proof check. We first check if the first tree’s root hash value         is present in the second tree:
      1. If present, we find its sibling, compute its hash value, add the hash to the output list, compute its parent and then repeat            the process till we end up at the root of the second tree. This will give us all the intermediate node’s hash values. In the            end, this intermediate node list along with the hashes of the first tree and second tree is printed. 
      2. If not present, then we find the left child of root of first tree which we will refer to as “lc , right child of root of first          tree and the sibling of this right child in second tree. This right child and its sibling are combined to form the sibling of           "lc". We will refer to this sibling as “rc”. We then proceed in the same manner as the above step, computing the parent of               "lc" and "rc", adding this hash value to the output list and then repeating the process till we end up at the root of the               second tree. This gives us all the hashes of the intermediate nodes and this list in addition to the hashes of the roots of             first tree and second tree are printed.

Screenshots:
![checkconsistency screenshot 1](https://github.com/droid76/Merkle-Tree/blob/master/Screenshots/checkconsistency-1.png)
![checkconsistency screenshot 2](https://github.com/droid76/Merkle-Tree/blob/master/Screenshots/checkconsistency-2.png)
