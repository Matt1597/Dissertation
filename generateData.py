import matplotlib.pyplot as plt
import math
import numpy as np
from numpy.linalg import norm
import random
import pandas as pd
from functools import reduce
import scipy.cluster
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
import json
##22 good
random.seed(50)
radius = []
mat = np.array(pd.read_csv("SimMatrix25-1.csv",header = None))

for x in range(len(mat[0])):
    for y in range(len(mat[0])):
        if(mat[x][y] == mat[y][x]):
            mat[x][y] = 0
        mat[x][y] = mat[y][x]

print(mat)


dists = squareform(mat)
linkage_matrix = linkage(dists, "ward")
l = linkage_matrix
print(linkage_matrix)
print(linkage_matrix[1][1])
labs = []
for x in range(len(linkage_matrix)+1):
    labs.append(x)
    radius.append(random.randint(3,16))
print(labs)
T = scipy.cluster.hierarchy.to_tree( linkage_matrix , rd=False )
dendrogram(linkage_matrix, labels=labs)


print(len(linkage_matrix))

print(radius)
#Save linkage matrix
a = []
l = [1,2,3,4]
linkage_matrix = np.insert(linkage_matrix, 0, l, axis=0)


size = list(radius)
id2size = dict(zip(range(len(size)), size))

def add_node(node, parent ):

	newNode = dict( node_id=node.id, children=[] )
	parent["children"].append( newNode )


	if node.left: add_node( node.left, newNode )
	if node.right: add_node( node.right, newNode )


d3Dendro = dict(children=[], name="Root1")
add_node( T, d3Dendro )


def size_tree( n ):

    if len(n["children"]) == 0:
           leafSize = [id2size[n["node_id"]]]


    else:
           leafSize = reduce(lambda ls, c: ls + size_tree(c), n["children"], [])

    n["size"] = size = "-".join(sorted(map(str, leafSize)))



    return leafSize

size_tree( d3Dendro["children"][0])

# Output Data
json.dump(d3Dendro, open("pack/d3-dendrogram.json", "w"), sort_keys=True, indent=4)
np.savetxt("force/linkage.csv", linkage_matrix, delimiter=",",fmt="%s")
np.savetxt("agglomerative+force/linkage.csv", linkage_matrix, delimiter=",",fmt="%s")
np.savetxt("agglomerative/linkage.csv", linkage_matrix, delimiter=",",fmt="%s")
np.savetxt("radius.txt", radius, delimiter=",",fmt="%s")
plt.title("Dendrogram")
plt.show()
#fig.savefig('plotcircles.png')
