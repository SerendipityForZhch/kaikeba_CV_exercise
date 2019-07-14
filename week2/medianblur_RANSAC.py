# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 12:05:08 2019

@author: HP
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt
import random
import math



def medianBlur(img, kernel, padding_way):
    img_rows,img_cols = len(img),len(img[0])
    knl_rows,knl_cols = len(kelnel),len(kelnel[0])
    if(padding_way == "REPLICA"):
        padd_img = [(knl_cols//2)*[img[row][0]] + img[row] + (knl_cols//2)*[img[row][-1]] for row in range(img_rows)]
        for col in range(knl_cols//2):
            padd_img.insert(0,padd_img[0])
            padd_img.append(padd_img[-1])
        
    elif(padding_way == "ZERO"):
        padd_img = [(knl_cols//2)*[0] + img[row] + (knl_cols//2)*[0] for row in range(img_rows)]
        for col in range(knl_cols//2):
            padd_img.insert(0,len(padd_img[0])*[0])
            padd_img.append(len(padd_img[0])*[0])
        
    else:
        padd_img = [[]]
        print("No such padding way!")
        return padd_img
    print("padded img:rows:{0} , cols:{1}".format(len(padd_img) , len(padd_img[0])))
    for i in range(knl_rows//2 , img_rows+knl_rows//2):
        for j in range(img_cols//2 , img_cols+knl_cols//2):
            l = [padd_img[i-knl_rows//2 + kr][j-knl_cols//2 + kc] for kc in range(knl_cols) for kr in range(knl_rows)]
            sortedl = sorted(l)
            img[i-knl_rows//2][j-knl_cols//2] = sortedl[len(l)//2] ###it seems only half part is blured.why???
    return img





if __name__ == "__main__":
    ###Image blur
    img_lena = cv2.imread("lena.jpg",cv2.IMREAD_GRAYSCALE)
    kelnel = np.ones((7,7))
    imglist = [list(img_lena[i,:]) for i in range(img_lena.shape[0])]
    knllist = [list(kelnel[i,:]) for i in range(kelnel.shape[0])]
    print("img:rows:{0} , cols:{1}".format(len(imglist) , len(imglist[0])))

    blurimg = medianBlur(imglist,knllist,"REPLICA")
    blur_array = np.array(blurimg)
    print("blurimg:rows:{0} , cols:{1}".format(blur_array.shape[0] , blur_array.shape[1]))
    cv2.imshow("blur",blur_array)
    cv2.imshow("lenna_gray",img_lena)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    ###RANSAC : to model a line using random dataset
    SIZE = 50
    x = np.linspace(0,10,SIZE)
    y = 3 * x + 1
    randomx = []
    randomy = []
    for i in range(SIZE):
        randomx.append(x[i] + random.uniform(-0.5,0.5)) #random noise
        randomy.append(y[i] + random.uniform(-0.5,0.5))
    for i in range(SIZE):
        randomx.append(x[i] + random.uniform(0,10)) #regarded as outliers
        randomy.append(y[i] + random.uniform(1,30))
    
    RandomX = np.array(randomx)
    RandomY = np.array(randomy)
    
    #use RANSAC to estimate the parameters of the linear model
    iters = 1000
    sigma = 0.2 #error threshold
    p = 0.9 #the propability of getting the good model
    preinliers = 0
    
    for i in range(iters):
        randidx = random.sample(range(2*SIZE) ,2)
        x1 = RandomX[randidx[0]]
        y1 = RandomY[randidx[0]]
        x2 = RandomX[randidx[1]]
        y2 = RandomY[randidx[1]]
        a = (y2-y1)/(x2-x1)
        b = y2 - a*x2 #the current guessed model
        
        inliers = 0
        for j in range(2*SIZE):
            if(abs(a*RandomX[j]+b - RandomY[j]) < sigma):
                inliers += 1
        if(inliers > preinliers):
            besta = a
            bestb = b
            preinliers = inliers
            iters = math.log(1 - p) / math.log(1 - pow(inliers / (SIZE * 2), 2)) #update the iters according to current model
        if(inliers > SIZE):
            break;
    
    Y = besta * RandomX + bestb
    print("linear model: a:{0} , b:{1}".format(besta,bestb))
    plt.scatter(RandomX,RandomY)
    plt.scatter(RandomX,Y)
    
    plt.show()
    
    
