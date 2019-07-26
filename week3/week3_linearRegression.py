# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 19:34:24 2019

@author: HP
"""

import numpy as np
import random
import matplotlib.pyplot as plt

def inference(w, b, x):        # inference, test, predict, same thing. Run model after training
    pred_y = w * x + b
    return pred_y

def eval_loss_np(w, b, x_list, gt_y_list):
    avg_loss = 0.0
    #print(w,b,len(x_list) , len(gt_y_list))
    loss_arr =  0.5 * (w * x_list + b - gt_y_list) ** 2
    avg_loss = loss_arr.sum()
    avg_loss /= len(gt_y_list)
    return avg_loss

def gradient(pred_y, gt_y, x):
    diff = pred_y - gt_y
    dw = diff * x
    db = diff
    return dw, db

def cal_step_gradient_np(batch_x_list, batch_gt_y_list, w, b, lr):
    avg_dw, avg_db = 0, 0
    batch_size = len(batch_x_list)
    
    pred_y = inference(w,b,batch_x_list)
    dw,db = gradient(pred_y, batch_gt_y_list, batch_x_list)
    
    avg_dw = dw.sum()
    avg_db = db.sum()
    #print("dw:{0} , db:{1}".format(avg_dw,avg_db))
    avg_dw /= batch_size
    avg_db /= batch_size
    w -= lr * avg_dw
    b -= lr * avg_db
    return w, b

def train_np(x_list, gt_y_list, batch_size, lr, max_iter):
    w = 0
    b = 0
    num_samples = len(x_list)
    for i in range(max_iter):
        batch_idxs = np.random.choice(len(x_list), batch_size)
        batch_x = x_list[batch_idxs]
        batch_y = gt_y_list[batch_idxs]
        w, b = cal_step_gradient_np(batch_x, batch_y, w, b, lr)
        print('w:{0}, b:{1}'.format(w, b))
        print('loss is {0}'.format(eval_loss_np(w, b, x_list, gt_y_list)))

def gen_sample_data_np():
    #w = random.randint(0, 10) + random.random()		# for noise random.random[0, 1)
    #b = random.randint(0, 5) + random.random()
    w = 3 + random.random()		# for noise random.random[0, 1)  ###sometimes the loss is exploding with the fixed learning rate
    b = -1 + random.random()
    num_samples = 100
    x_array = np.random.randint(0,100,size=num_samples)*np.random.random()
    y_array = x_array * w + b + np.random.random()*np.random.randint(-1,1)
    return x_array , y_array , w , b

def run():
    x_list, y_list, w, b = gen_sample_data_np()
    plt.scatter(x_list,y_list)
    plt.show()
    print(w,b)
    lr = 0.005
    max_iter = 100
    train_np(x_list, y_list, 50, lr, max_iter)

if __name__ == '__main__':	# 跑.py的时候，跑main下面的；被导入当模块时，main下面不跑，其他当函数调
    run() 