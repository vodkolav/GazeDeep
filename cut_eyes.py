#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cuts rectangular eyes region from image of face
  img -- the image to work with can be either a path to img (str) or array containing image data
  to_size -- size of resulting image in pixels (width, height)
  dest_path --(optional) where to save the resulting image
  show -- (optional whether to display the result in a separate window)
  
  #based on code from:
  #https://stackoverflow.com/questions/20425724/pythonopencv-cv2-imwrite
  
@author: Michael Berger
"""

import cv2
from sys import stdout
from conf import path

face_cascade = cv2.CascadeClassifier(str(path/'models/haarcascade_frontalface_default.xml'))                             
#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier(str(path/'models/haarcascade_eye.xml'))
#eye_cascade = cv2.CascadeClassifier(str(path/'models/haarcascade_eye_tree_eyeglasses.xml')


def report(what):
  """
  like print() but reports on the same line so that output doesn't end up cluttered
  """
  stdout.write("\r%s" % what)
  stdout.flush()


def cut_eyes(img, to_size = (160,60), dest_path = None, show = False):
  """
  Cuts rectangular eyes region from image of face
  img -- the image to work with can be either a path to img (str) or array containing image data
  to_size -- size of resulting image in pixels (width, height)
  dest_path --(optional) where to save the resulting image
  show -- (optional whether to display the result in a separate window)
  """
  if(type(img)==str):
    img = cv2.imread(img)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  for (x,y,w,h) in faces:        
      roi_gray = gray[y:y+h, x:x+w]              
      eyes = eye_cascade.detectMultiScale(roi_gray)   
      eyes = eyes[0:2,] #sometimes it detects 3 eyes. so take just the first 2
      ((ex1,ey1,ew1,eh1),(ex2,ey2,ew2,eh2)) = eyes #tuple umpacking ftw
      #instead of square around each eye take a rectangle around both ov them      
      (x1,y1,x2,y2) = (min(ex1,ex2), min(ey1,ey2), max(ex1+ew1,ex2+ew2), max(ey1+eh1,ey2+eh2))   
      roi_color = img[y:y+h, x:x+w]  #roi is for region of interest
      img = cv2.resize(roi_color[y1:y2, x1:x2], to_size)
  if show:      
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
    cv2.rectangle(roi_color,(x1,y1),(x2,y2),(0,255,0),2)
    cv2.imshow('img',roi_color)  
  if(dest_path != None):      
    cv2.imwrite(dest_path,img)
  return img


##test on single file 

#print(path)
#fname = 'frame1586.jpg'
#lal = path/'eyetrack'/fname
#lal.suffix
#
#eyes_cut = cut_eyes(str(path/'eyetrack'/fname), show = 0)
#cv2.imshow('hi',eyes_cut)

def cut_eyes_dir(src_dir_path, dest_dir_path):  
  """
  performs cut_eyes on all files in a directory
  """
  if (src_dir_path == dest_dir_path):
    raise FileExistsError("source an dest folders must be different!")
  if(input("This will overwrite any files in destination directory. Are you sure?")!="y"):
    print("aborted")
    return
  print("cutting eyes")
  for fl in sorted(src_dir_path.iterdir()):
    if fl.suffix == '.jpg':
      report('processing file ' + fl.name)    
      cut_eyes(str(fl), dest_path= str(dest_dir_path/fl.name))

#test on a directory
#cut_eyes_dir(path/'eyetrack' ,path/'eyetrack_eyes')


  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  