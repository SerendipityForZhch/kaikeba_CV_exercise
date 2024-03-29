# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 21:24:14 2019

@author: HP
"""

import cv2
import numpy as np
import random
from matplotlib import pyplot as plt
from math import *

class CvImg():
    def __init__(self,img):
        self.img = img
    
    def getShape(self):
        return self.img.shape
    
    def showImg(self):
        cv2.imshow("imgobj",self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def splitImg(self):
        B,G,R = cv2.split(self.img)
        return B,G,R
    
    def changeBrightness(self , lighten , factor):#lighten=1,变亮facter percents ; lighten=0,变暗facter percents
        rows , cols , chas = self.getShape()
        if(lighten == 1):
            factor = 1 + factor
        elif(lighten == 0):
            factor = 1 - factor
        else:
            print("wrong opcodes!")
        for i in range(rows):
            for j in range(cols):
                self.img[i][j][0] = self.img[i][j][0] * factor
                self.img[i][j][1] = self.img[i][j][1] * factor
                self.img[i][j][2] = self.img[i][j][2] * factor
                self.img[i][j][self.img[i][j] > 255] = 255
        self.showImg()
    
    def reverseColor(self): #翻转每个像素点
        table = []
        for i in range(256):
            table.append(255 - i)
        table = np.array(table).astype("uint8")
        self.img = cv2.LUT(self.img , table)
        self.showImg()
    
    def equalizeImg(self): #对每个通道像素值进行均衡
        print("original histgram:")
        #plt.hist(img_brighter.flatten(), 256, [0, 256], color = 'r')
        #plt.hist(self.img.flatten() , 256, [0, 256], color = 'r')
        plt.hist(np.array(self.splitImg()[0]).flatten() , 256, [0, 256], color = 'b')
        plt.hist(np.array(self.splitImg()[1]).flatten() , 256, [0, 256], color = 'g')
        plt.hist(np.array(self.splitImg()[2]).flatten() , 256, [0, 256], color = 'r')
        
        eq_b = cv2.equalizeHist(self.img[:,:,0])
        eq_g = cv2.equalizeHist(self.img[:,:,1])
        eq_r = cv2.equalizeHist(self.img[:,:,2])
        
        self.img = cv2.merge((eq_b,eq_g,eq_r))
        self.showImg()
        
    def rotateImg(self,rad,scale):#围绕图片中心进行旋转，保持图片不被裁剪
        """
        rows,cols,chas = self.getShape()
        M = cv2.getRotationMatrix2D(center,rad,scale)
        rot_img = cv2.warpAffine(self.img, M, (rows, cols))
        cv2.imshow("rotimg",rot_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        """
        height, width = self.getShape()[:2]
        heightNew = int(width * fabs(sin(radians(rad))) + height * fabs(cos(radians(rad))))
        widthNew = int(height * fabs(sin(radians(rad))) + width * fabs(cos(radians(rad))))
    
        matRotation = cv2.getRotationMatrix2D((width / 2, height / 2), rad, 1)
        #matRotation = cv2.getRotationMatrix2D((0 , 0), rad, 1)
    
        matRotation[0, 2] += (widthNew - width) / 2
        matRotation[1, 2] += (heightNew - height) / 2
        
        imgRotation = cv2.warpAffine(self.img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))
        cv2.imshow("rotimg",imgRotation)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
        # perspective transform
    def persTrans(self,rand,pts1=None,pts2=None): #rand=1:随机进行透视变换 ； rand=0:按指定的位置点进行变换
        height, width, channels = self.img.shape
    
        if(rand==1):
            random_margin = 60
            x1 = random.randint(-random_margin, random_margin)
            y1 = random.randint(-random_margin, random_margin)
            x2 = random.randint(width - random_margin - 1, width - 1)
            y2 = random.randint(-random_margin, random_margin)
            x3 = random.randint(width - random_margin - 1, width - 1)
            y3 = random.randint(height - random_margin - 1, height - 1)
            x4 = random.randint(-random_margin, random_margin)
            y4 = random.randint(height - random_margin - 1, height - 1)
        
            dx1 = random.randint(-random_margin, random_margin)
            dy1 = random.randint(-random_margin, random_margin)
            dx2 = random.randint(width - random_margin - 1, width - 1)
            dy2 = random.randint(-random_margin, random_margin)
            dx3 = random.randint(width - random_margin - 1, width - 1)
            dy3 = random.randint(height - random_margin - 1, height - 1)
            dx4 = random.randint(-random_margin, random_margin)
            dy4 = random.randint(height - random_margin - 1, height - 1)
        
            pts1 = np.float32([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
            pts2 = np.float32([[dx1, dy1], [dx2, dy2], [dx3, dy3], [dx4, dy4]])
            
        elif(rand==0):
            pts1 = np.float32([ list(i) for i in pts1])
            pts2 = np.float32([ list(i) for i in pts2])
        else:
            print("Wrong opcode")
        
        M_warp = cv2.getPerspectiveTransform(pts1, pts2)
        img_warp = cv2.warpPerspective(self.img, M_warp, (width, height))
            
        cv2.imshow("rotimg",img_warp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

            




if __name__ == "__main__":
    img_color = cv2.imread("ball.jpg")
    ImgObj = CvImg(img_color)
    ImgObj.showImg()
    ImgObj.changeBrightness(1,0.2)
    ImgObj.reverseColor()
    ImgObj.equalizeImg()
    ImgObj.rotateImg(30,1)
    p1 = [(0,0),(0,10),(10,0),(10,10)]
    p2 = [(0,0),(0,10),(10,0),(12,12)]
    ImgObj.persTrans(0,p1,p2)