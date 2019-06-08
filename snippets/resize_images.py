#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:32:24 2019

@author: michael
"""

import cv2
import pathlib


path = pathlib.Path("/home/michael/Code/video")
path




#list(path.glob('*.jpg'))

fname = 'frame124.jpg'
lal = path/'eyetrack'/fname
lal.suffix
#src_path = str(fname)

def resize_img(src_path, to_size = (160,120), dest_path = None, show = False):
  img = cv2.imread(src_path)
  imgres = cv2.resize(img, to_size)
  if show:
    cv2.namedWindow(str(img.shape),1)
    cv2.imshow(str(img.shape),  img)
    cv2.namedWindow(str(imgres.shape),1)
    cv2.imshow(str(imgres.shape), imgres)
  if(not dest_path ==None):
    cv2.imwrite(dest_path,imgres)
  return imgres

#x = resize_img(str(path/'eyetrack'/fname),to_size= (480,360), dest_path= str(path/'eyetrack_small'/fname))





for fl in (path/'eyetrack').iterdir():
  if fl.suffix == '.jpg':
    resize_img(str(fl), dest_path= str(path/'eyetrack_small'/fl.name))
    print('{0}'.format(fl.name), end="\r")

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  