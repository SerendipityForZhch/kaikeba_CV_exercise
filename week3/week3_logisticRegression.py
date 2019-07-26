# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 19:37:36 2019

@author: HP
"""
import numpy as np
import random
import matplotlib.pyplot as plt

def gen_sample_data_lr():
    num_samples = 100
    x1 = np.linspace(0,5,num_samples//2) + np.random.randint(-1,1)*np.random.random()
    x2 = np.linspace(5,10,num_samples//2) + np.random.randint(-1,1)*np.random.random()
    x = np.hstack((x1,x2))
    y = x > 5
    return x,y

def inference_lr(w,b,x_arr):
    predict_y = 1/(1+np.exp(-1*(w*x_arr + b)))
    return predict_y

def gradient_lr(pred_y, gt_y, x):
    diff = pred_y - gt_y
    dw = diff * x
    db = diff
    return dw, db

def cal_step_gradient_lr(batch_x_list, batch_gt_y_list, w, b, lr):
    avg_dw, avg_db = 0, 0
    batch_size = len(batch_x_list)
    
    pred_y = inference_lr(w,b,batch_x_list)
    dw,db = gradient_lr(pred_y, batch_gt_y_list, batch_x_list)
    
    avg_dw = dw.sum()
    avg_db = db.sum()
    
    #print("dw:{0} , db:{1}".format(avg_dw,avg_db))
    avg_dw /= batch_size
    avg_db /= batch_size
    w -= lr * avg_dw
    b -= lr * avg_db
    return w, b


def eval_loss_lr(w, b, x_list, gt_y_list):
    avg_loss = 0.0
    #print(w,b,len(x_list) , len(gt_y_list))
    loss_arr =  -1*gt_y_list*np.log(1/(1+np.exp(-1*w*x_list - b))) - (1-gt_y_list)*np.log(1-(1/(1+np.exp(-1*w*x_list - b))))
    avg_loss = loss_arr.sum()
    avg_loss /= len(gt_y_list)
    return avg_loss


def train_lr(x_list, gt_y_list, batch_size, lr, max_iter):
    w = 0
    b = 0
    num_samples = len(x_list)
    
    for i in range(max_iter):
        batch_idxs = np.random.choice(len(x_list), batch_size)
        batch_x = x_list[batch_idxs]
        batch_y = gt_y_list[batch_idxs]
        w, b = cal_step_gradient_lr(batch_x, batch_y, w, b, lr)
        print('w:{0}, b:{1}'.format(w, b))
        print('loss is {0}'.format(eval_loss_lr(w, b, x_list, gt_y_list)))
    x = np.linspace(0,10,100)
    y = (1/(1+np.exp(-1*w*x - b)))
    plt.scatter(x,y)
    plt.show()
    
def run_lr():
    x_list, y_list = gen_sample_data_lr()
    plt.scatter(x_list,y_list)
    plt.show()

    lr = 0.1
    max_iter = 800
    train_lr(x_list, y_list, 50, lr, max_iter)
    
if __name__ == '__main__':	# 跑.py的时候，跑main下面的；被导入当模块时，main下面不跑，其他当函数调
    run_lr() 