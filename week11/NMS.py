# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 23:14:41 2019

@author: HP
"""

def getiou(boundA, boundB):
    ax1, ay1, ax2, ay2 = boundA
    bx1, by1, bx2, by2 = boundB
    
    assert ax2 > ax1 and ay2 > ay1
    assert bx2 > bx1 and by2 > by1
    square_a = (ax2 - ax1) * (ay2 - ay1)
    square_b = (bx2 - bx1) * (by2 - by1)
    
    if((abs(ax1-bx1) >= (ax2-ax1)) or
       (abs(ax1-bx1) >= (bx2-bx1)) or
       (abs(ay1-by1) >= (ay2-ay1)) or
       (abs(ay1-by1) >= (by2-by1))):
        return 0
    if((ax1<=bx1<=ax2) and (ay1<=by1<=ay2)):
        aera = (ax2 - bx1) * (ay2 - by1)
    elif((ax1<=bx1<=ax2) and (ay1<=by2<=ay2)):
        aera = (ax2 - bx1) * (by2 - ay1)
    elif((bx1<=ax1<=bx2) and (ay1<=by1<=ay2)):
        aera = (bx2 - ax1) * (ay2 - by1)
    elif((bx1<=ax1<=bx2) and (ay1<=by2<=ay2)):
        aera = (bx2 - ax1) * (by2 - ay1)
    else:
        aera = 0
    return aera/(square_a + square_b - aera)*1.0
        
    
    
    
class NMS(object):
    def __init__(self, boxes, thre):
        bounds = list(map(tuple, boxes[0:-1]))
        scores = boxes[-1]
        boxlists = list(zip(bounds, scores))
        f = lambda x:x[1]
        self.boxlists = sorted(boxlists, key = f, reverse=True)
        self.boxnum = len(self.boxlists)
        self.thre = thre
        self.outlists = []
    
    def out(self):
        indexs = list(range(self.boxnum))
        while(indexs != []):
            maxidx = indexs.pop(0)
            self.outlists.append(self.boxlists[maxidx])
            for i in range(len(indexs)):
                #print(i)
                iou = getiou(self.boxlists[maxidx][0], self.boxlists[indexs[i]][0])
                #print(self.boxlists[maxidx][1], self.boxlists[indexs[i]][1], iou)
                if iou > self.thre:
                    _ = indexs.pop(i)
        
        return self.outlists
            

if __name__ == '__main__':
    bound1, bound2, bound3, bound4, bound5 = [0, 0, 2, 2], [1, 1, 3, 3], [2, 2, 4, 4], [3, 3, 5, 5], [4, 4, 6, 6]
    scores = [0.9, 0.45, 0.85, 0.6, 0.75]
    boxes = [bound1, bound2, bound3, bound4, bound5, scores]
    
    myNMS = NMS(boxes, 0.1)
    print(myNMS.boxlists)
    print(myNMS.out())
    
    
    
