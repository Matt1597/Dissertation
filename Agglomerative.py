##############################################
#Authors: Matthew Reilly
#16/04/2019
#What it does:
#agglomerative clustering algorithm

##############################################

#libaries
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

#variales
PRECISION = 5
colour = ["red","purple","yellow","green","red","cyan","orange","gray","red","purple","yellow","green","red","cyan","orange","gray","red","purple","yellow","green","red","cyan","orange","gray"]
cluster = 0

#define aspect ratio
aspectX = 16
aspectY = 9

#input the radii
f = open('radius.txt', 'r')
radius = f.read().split('\n')
f.close()

#import the linkage matrix
linkage_matrix = np.array(pd.read_csv("agglomerative/linkage.csv",header = None))
linkage_matrix = np.delete(linkage_matrix, (0), axis=0)
cout=0

#create a new group
def new_group():
    group = []
    group.append([])
    group.append([])
    group.append([])
    group.append([])
    group.append([])
    group.append([])
    return group

#add circle to group of many
def Circle(group,x, y, radius, label):
    #0 = x coordinate
    #1 = y coordinate
    #2 = radius
    #3 = label
    #4 = cluster
    #5 = homogeneous coordinate
    group[0].append(x)
    group[1].append(y)
    group[2].append(radius)
    group[3].append(label)
    group[4].append(0)
    group[5].append(1)
    return group

#join one circle to another
def one_to_one(group,circle1, radius, label):
    Circle(group,circle1[2]+radius,0,radius, label)
    return group

#calculate where the circle interects with the group1
def circle_intersect(circle1, circle2,radius):


    X1, Y1 = circle1[0], circle1[1]
    X2, Y2 = circle2[0], circle2[1]
    R1, R2 = circle1[2]+radius, circle2[2]+radius

    Dx = X2-X1
    Dy = Y2-Y1
    D = round(math.sqrt(Dx**2 + Dy**2), PRECISION)
    if D > R1 + R2:
        return [0,0]
    elif D < math.fabs(R2 - R1):
        return [0,0]
    elif D == 0 and R1 == R2:
        return [0,0]
    else:
        a = (R1**2 - R2**2 + D**2)/(2*D)
        # distance from 1st circle's centre to the chord between intersects
        h = math.sqrt(R1**2 - a**2)
        midx = X1 + (a*Dx)/D
        midy = Y1 + (a*Dy)/D
        I1 = (round(midx + (h*Dy)/D, PRECISION),
              round(midy - (h*Dx)/D, PRECISION))

        #I2 = (round(midx - (h*Dy)/D, PRECISION),
        #      round(midy + (h*Dx)/D, PRECISION))


        return I1;

#check if there are any intersection when join one to many
def check_intersection(group,point,r):
    for x in range(len(group[0])):
        Dx = point[0]-group[0][x]
        Dy = point[1]-group[1][x]
        D = round(math.sqrt(Dx**2 + Dy**2), PRECISION)
        if D < r+group[2][x]:
            return bool(False)
    return bool(True)

#check if there are any intersection when join many to many
def check_intersection_many(group1,group2):
    for i in range(len(group1[0])):
        for j in range(len(group2[0])):
            Dx = group2[0][j]-group1[0][i]
            Dy = group2[1][j]-group1[1][i]
            D = round(math.sqrt(Dx**2 + Dy**2), PRECISION)
            if D < group1[2][i]+group2[2][j]:
                return bool(False)
    return bool(True)

#loop for all pairs
    #get the circle intersect
    #check for intersections
    #if no overlaps
        #get shortest distance between points
#pair with shortest distance between max join
#
#
#
def add_circle(group,r,label):
    minD = math.inf
    minI = 0
    minJ = 0
    for i in range(len(group[0])):
        for j in range(len(group[0])):
            if i != j:
                intersection = circle_intersect([row[i] for row in group],[row[j] for row in group],r)
                if isinstance(intersection[0], float):
                    if check_intersection(group,intersection,r):
                        D = shortest_distance(group,intersection,r)
                        if(D<minD):
                            minD = D
                            minI = i
                            minJ = j
    intersection = circle_intersect([row[minI] for row in group],[row[minJ] for row in group],r)
    #print(intersection)
    Circle(group,intersection[0],intersection[1],r, label)
    return group

#calulate the shortest distant many
def shortest_distance(group,point,r):
    maxD = 0
    for i in range(len(group[0])):
        for j in range(len(group[0])):
            if i != j:
                Dx = point[0]-group[0][i]*aspectY
                Dy = point[1]-group[1][i]*aspectX
                D = round(math.sqrt(Dx**2 + Dy**2), PRECISION)+r+group[2][i]
                if D>maxD:
                    maxD = D

                Dx = group[0][j]-group[0][i]*aspectY
                Dy = group[1][j]-group[1][i]*aspectX
                D = round(math.sqrt(Dx**2 + Dy**2), PRECISION)+group[2][i]+group[2][i]
                if D>maxD:
                    maxD = D

    return maxD

#calulate the shortest distant many
def shortest_distance_many(group1,group2):
    group = np.concatenate((group1,group2),1)
    maxD = 0
    for i in range(len(group[0])):
        for j in range(len(group[0])):
            if i != j:

                Dx = group[0][j]-group[0][i]*aspectY
                Dy = group[1][j]-group[1][i]*aspectX
                D = round(math.sqrt(Dx**2 + Dy**2), PRECISION)+group[2][i]+group[2][i]
                if D>maxD:
                    maxD = D
    return maxD
#rotate group
def rotate(group, radians):
    theta = np.radians(radians)
    c,s = np.cos(theta), np.sin(theta)
    rMatrix = [[c,s,0,0,0,0],[-s,c,0,0,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]]

    group = np.dot(rMatrix,group)
    return group

#calulate the rotation angle needed to rotate group to correct place
def get_rotation_angle(p0,p1,p2):

    d = np.arctan2(p1[1],p1[0])
    e =  np.arctan2(p2[1],p2[0])

    angle = d-e
    return (180/np.pi)*angle
#translate a group to a new coordinate
def translate(group,x,y):
    tMatrix =[[1,0,0,0,0,x],[0,1,0,0,0,y],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]]
    group = np.dot(tMatrix,group)

    return group

#for each pair in group1
#   for each circle in group2
#       get circle intersect
#       rotate and translate
#       check for intersections
#       if no overlaps
#           get shortest distance between points
#pair with shortest distance between max join
#
def manyToMany(group1,group2):
    minDistance = math.inf
    minGroup = []

    for a in range(len(group1[0])):
        for b in range(len(group1[0])):
            if a != b:
                for c in range(len(group2[0])):
                    for d in range(len(group2[0])):
                        if c != d:
                            intersectionC = circle_intersect([row[a] for row in group1],[row[b] for row in group1],group2[2][c])
                            if isinstance(intersectionC[0], float):
                                if check_intersection(group1,intersectionC,group2[2][c]):
                                    intersectionD = circle_intersect([row[a] for row in group1],[intersectionC[0],intersectionC[1],group2[2][c],1],group2[2][d])
                                    if isinstance(intersectionD[0], float):
                                        if check_intersection(group1,intersectionD,group2[2][d]):
                                            x = group2[0][c]
                                            y = group2[1][c]
                                            x1 = intersectionC[0]
                                            y1 = intersectionC[1]

                                            group3 = translate(group2,-x,-y)
                                            rotation_angle = get_rotation_angle((group3[0][c],group3[1][c]),(group3[0][d],group3[1][d]),(intersectionD[0]-x1,intersectionD[1]-y1))
                                            group3 = rotate(group3,rotation_angle)
                                            group3 = translate(group3,intersectionC[0],intersectionC[1])

                                            if check_intersection_many(group1,group3):
                                                reverse = 0
                                                D = shortest_distance_many(group1,group3)
                                                if D < 0:
                                                    D = D*-1
                                                    reverse = 1
                                                if(D<minDistance):
                                                    minDistance = D
                                                    minGroup = group3


    group3 = np.concatenate((group1,minGroup),1)

    return group3
#print concept map using pyplot
def printGroup(group):

    #print graph
    ax = plt.gca()
    for x in range(len(group[0])):
        ax.add_patch(plt.Circle((group[0][x], group[1][x]), group[2][x], color=colour[int(group[4][x])]))
        plt.annotate(int(group[3][x]), (group[0][x],group[1][x]))



#Main loop what uses the linkage matrix to create the concept map
groups = []
#for every connection in linkage matrix
for x in range(len(linkage_matrix)):
    # if both a leaves then join one to one
    if(linkage_matrix[x][0] < len(linkage_matrix)+1 and linkage_matrix[x][1] < len(linkage_matrix)+1):
        circles = new_group()
        circles = Circle(circles,0,0,int(radius[cout]), linkage_matrix[x][0])
        cout = cout+1
        circles = one_to_one(circles,[row[0] for row in circles],int(radius[cout]), linkage_matrix[x][1])
        cout = cout+1
    #if one is a group and then join one to many
    elif(linkage_matrix[x][0] < len(linkage_matrix)+1 and linkage_matrix[x][1] >= len(linkage_matrix)+1):
        circles = groups[int(linkage_matrix[x][1]-(len(linkage_matrix)+1))]

        circles = add_circle(circles, int(radius[cout]), linkage_matrix[x][0])
        cout = cout+1
    #if one is a group and then join one to many
    elif(linkage_matrix[x][0] >= len(linkage_matrix)+1 and linkage_matrix[x][1] < len(linkage_matrix)+1):
        circles = groups[int(linkage_matrix[x][0]-(len(linkage_matrix)+1))]

        circles = add_circle(circles, int(radius[cout]), linkage_matrix[x][1])
        cout = cout+1
    #if both are groups then join many to many
    elif(linkage_matrix[x][0] >= len(linkage_matrix)+1 and linkage_matrix[x][1] >= len(linkage_matrix)+1):


        group1 = groups[int(linkage_matrix[x][0]-(len(linkage_matrix)+1))]
        group2 = groups[int(linkage_matrix[x][1]-(len(linkage_matrix)+1))]
        #if the linkage matrix is above 0.7 similarity then make that a cluster
        if(linkage_matrix[x][2] > 0.7):
            found1 = 0
            found2 = 0
            for y in range(len(group1[0])):
                if group1[4][y] == 0:
                    if(found1 == 0):
                        cluster = cluster + 1
                        found1 = 1
                    group1[4][y] = cluster

            for z in range(len(group2[0])):
                if (group2[4][z] == 0):
                    if(found2 == 0):
                        cluster = cluster + 1
                        found2 = 1
                    group2[4][z] = cluster


        circles = manyToMany(group1,group2)


    groups.append(circles)



printGroup(groups[len(groups)-1])



a = []
#format for output
for i in range(len(groups[len(groups)-1][1])):
    a.append(i)
np.set_printoptions(suppress=True)
groups[len(groups)-1] = np.insert(groups[len(groups)-1], 0, a, axis=0)



#output to files to use in d3.js
a = np.asarray(groups[len(groups)-1])
np.savetxt("agglomerative/array.csv", a, delimiter=",",fmt='%f')
np.savetxt("force/array.csv", a, delimiter=",",fmt='%f')
np.savetxt("agglomerative+force/array.csv", a, delimiter=",",fmt='%f')
plt.axis('scaled')
plt.show();
