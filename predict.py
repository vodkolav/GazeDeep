#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 17:38:33 2019

@author: michael
"""
# must install pytorch version 1.1.0 first
#conda install pytorch torchvision cudatoolkit=10.0 -c pytorch
#conda list | grep pytorch



from fastai.vision import defaults, torch, load_learner, Image, pil2tensor #open_image, 
import numpy  as np 
from conf import path
#import matplotlib.pyplot as plt
import cv2

defaults.device = torch.device('cpu')
model = load_learner(str(path/'models'), file = 'eyetrack_eyes_3.pkl')


def predict(cv2image):  
  
  cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
  
  img_fastai = Image(pil2tensor(cv2image, dtype=np.float32).div_(255)) 
  
  pred_class = model.predict(img_fastai)
  return(pred_class[0].data.round())
  #return(pred_class.data.round())

  
  
cv2im = cv2.imread(str(path/'data/eyetrack_eyes_2/frame123.jpg'))
pc = predict(cv2im)
  
  
  
#cv2im = cv2.cvtColor(cv2im, cv2.COLOR_BGR2RGB)
#cv2.imshow('image',cv2im)
#
#img_fastai = Image(pil2tensor(cv2im, dtype=np.float32).div_(255))
#print(type(img_fastai))
#
#img_fastai
#
#
#defaults.device = torch.device('cpu')
#
#
#img = open_image(path/'data/eyetrack_eyes_2/frame123.jpg')
#img
#print(type(img))
#
#learn = load_learner(str(path/'models'), file = 'eyetrack_eyes_3.pkl')
#
#
#pred_class,pred_idx,outputs = learn.predict(img_fastai)
#print(pred_class)
#print(pred_idx)
#print(outputs)





#conda list |grep fast*
