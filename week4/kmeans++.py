# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 22:26:42 2019

@author: HP
"""

import random
import math
import matplotlib.pyplot as plt

x1 = [random.randint(1,20) for i in range(12)]
y1 = [random.randint(60,80) for i in range(12)]
x2 = [random.randint(40,60) for i in range(12)]
y2 = [random.randint(20,40) for i in range(12)]
x3 = [random.randint(80,100) for i in range(12)]
y3 = [random.randint(30,50) for i in range(12)]

def zipdata(x,y):
    data = []
    for k in range(len(x)):
        data.append((x[k],y[k]))
    return data

testdata = []
testdata = testdata + zipdata(x1,y1)
testdata = testdata + zipdata(x2,y2)
testdata = testdata + zipdata(x3,y3)

plt.scatter([testdata[i][0] for i in range(len(testdata))] , [testdata[i][1] for i in range(len(testdata))])
plt.show()




class Kmeans:
    def __init__(self,data,K):
        self.K = K
        self.data = data
        self.memberOf = [-1 for i in range(len(self.data))]
        self.centers = [(0,0) for i in range(self.K)]
        self.loss = 0
        self.centerChgNum = 0
#         self.initcenters()
        self.init_improved()
        print(self.centers)
        self.assign()
        print(self.memberOf)
        
    
    def initcenters(self):
        for k in range(self.K):
            self.centers[k] = (random.randint(0,10) , random.randint(5,15)) #若某一类没有数据点，则update出错(division zero)
        self.centers[0] = (10,65)
        self.centers[1] = (50,55)
        self.centers[2] = (90,55)
        
            
    def init_improved(self):
        centroids = []
#         print(self.data)
        center = self.data[random.randint(0,len(self.data))]
        centroids.append(center)
        
        for k in range(1,self.K):
            weights = [self.closet(self.data[i] , centroids) for i in range(len(self.data))]
        
            total=sum(weights)
            weights=[x/total for x in weights]

            num=random.random()
            total=0
            x=-1
            while total<num:
                x+=1
                total+=weights[x]
            centroids.append(self.data[x])
        self.centers = centroids
        
    def closet(self,data,centers):
        mindis = 10000
        for k in range(len(centers)):
            dis = self.distance(data , centers[k])
            if(dis < mindis):
                mindis = dis
        return mindis
        
    def distance(self,a,b):
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    
    def assignOne(self,i):
        mindis = 100000
        for k in range(self.K):
            dis = self.distance(self.data[i] , self.centers[k])
            if(dis < mindis):
                centernum = k
                mindis = dis
        if(centernum != self.memberOf[i]):
            self.centerChgNum += 1
            self.memberOf[i] = centernum
        self.loss += mindis
    
    def assign(self):
        self.loss = 0
        self.centerChgNum = 0
        for k in range(len(self.data)):
            self.assignOne(k)
    
    def update(self):
#         members = [self.centers.count(i) for i in range(len(self.centers))]
        for k in range(self.K):
            member = self.memberOf.count(k)
            new_x = sum([self.data[i][0] for i in range(len(self.data)) if(self.memberOf[i] == k)])/member
            new_y = sum([self.data[i][1] for i in range(len(self.data)) if(self.memberOf[i] == k)])/member
            self.centers[k] = (new_x,new_y)
    
    def cluster(self):
        done = False
        while not done:
            self.update()
            self.assign()
            if(self.centerChgNum/len(self.memberOf) < 0.01):
                done = True
                print("loss:",self.loss)
    
    def printCluster(self):
        COLORS = ['red', 'blue', 'green']
        x1 = []
        y1 = []
        
        cluster = [[] for i in range(self.K)]
        for centroid in range(self.K):
            for k in range(len(self.data)):
                if(self.memberOf[k] == centroid):
                    cluster[centroid].append(self.data[k])
            plt.scatter(self.centers[centroid][0] ,self.centers[centroid][1], c=COLORS[centroid],linewidth=7)
            x = [cluster[centroid][i][0] for i in range(len(cluster[centroid]))]
            y = [cluster[centroid][i][1] for i in range(len(cluster[centroid]))]
            plt.scatter(x , y , c=COLORS[centroid],linewidth=4)
                
#         plt.scatter(self.centers[0][0] ,self.centers[0][1], c=COLORS[0],linewidth=7)
#         x = [cluster[0][i][0] for i in range(len(cluster[0]))]
#         y = [cluster[0][i][1] for i in range(len(cluster[0]))]
#         plt.scatter(x , y , c=COLORS[0],linewidth=4)
    
#         plt.scatter(self.centers[1][0] ,self.centers[1][1], c=COLORS[1],linewidth=7)
#         x = [cluster[1][i][0] for i in range(len(cluster[1]))]
#         y = [cluster[1][i][1] for i in range(len(cluster[1]))]
#         plt.scatter(x , y , c=COLORS[1],linewidth=4)
    
#         plt.scatter(self.centers[2][0] ,self.centers[2][1], c=COLORS[2],linewidth=7)
#         x = [cluster[2][i][0] for i in range(len(cluster[2]))]
#         y = [cluster[2][i][1] for i in range(len(cluster[2]))]
#         plt.scatter(x , y , c=COLORS[2],linewidth=4)
            
if __name__ == "__main__":
    kmeans = Kmeans(testdata,3)
    kmeans.cluster()
    print(kmeans.memberOf)
    kmeans.printCluster()
