#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main data gathering script 
Launches a game of bouncing ball.
The user gazes carefully at the ball with only the eyes, not turning the head.
The script takes pictures of the user's face from his laptop camera and selects only eyes region
The pictures and ball coordinates are saved.


@author: Michael Berger
"""


from tkinter import Tk, Canvas
import time
import cv2
from cut_eyes import cut_eyes
from conf import path, fullscreen
from aux import init_dir, output_dir
import random as rnd
from predict import predict

class Ball:  
  framenum = 0
  def __init__(self,canvas):
    
    self.canvas = canvas
    self.shape = canvas.create_oval(0, 0, BALLSIZE, BALLSIZE, fill=BALLCOLOR)
    self.speed = 30
    self.speedx = self.speed # changed from 3 to 9
    self.speedy = self.speed # changed from 3 to 9
    self.speed_range = [-15,15]
    self.active = True
    self.move_active()    
    canvas.bind_all('<Escape>', self.QuitProg)
     
    
  def randwalk(self,direction):
      return ((self.speed_range[1] - self.speed_range[0]) * rnd.random() + self.speed_range[0]) +direction
  
  def ball_update(self, position):    
    
    if PLAYMODE:
      self.canvas.coords(self.shape, position[0], position[1], position[0] + BALLSIZE,position[1] + BALLSIZE)    
    else:
      self.canvas.move(self.shape, self.speedx, self.speedy)    
      pos = self.canvas.coords(self.shape)
      if pos[1] <= 0:
          self.speedy = self.randwalk(self.speed)
      if pos[3] >= HEIGHT:
          self.speedy = self.randwalk(-self.speed)
      if pos[0] <= 0:
          self.speedx = self.randwalk(self.speed)
      if pos[2] >= WIDTH:
          self.speedx = self.randwalk(-self.speed)
    
 
  def move_active(self):
    if self.active:
      if PLAYMODE:
        position = play_frame()
        self.ball_update(position)   
      else:
        self.ball_update()
        self.framenum = record_frame(self.framenum, self.coord())        
      self.canvas.after(1, self.move_active) # changed from 10ms to 30ms
    else:
        tk.destroy()
          
  def QuitProg(self, evt):
        #self.canvas.destroy()
        self.active = False    
      
  def coord(self):
    x = self.canvas.coords(self.shape)
    return ','.join(str(int(e)) for e in x[0:2])


def record_frame(framenum,coord):
  try:
    ret, frame = cam.read()     
    eyes_found, frame = cut_eyes(frame)
    TOC = time.time() - TIC 
    #print(TOC)
    if TOC > MAXTIME: ball.QuitProg(None)
    if(eyes_found):

      cv2.imwrite(str(output_dir/("frame%d.jpg" % framenum)), frame)   #write to  images 'frame№.jpg'
      coordfile.write("%s,%s,%s\r\n" % (framenum, (str(coord)), TOC))  
      framenum = framenum + 1  # I intentionally disregard frames that failed to produce an eye region rectangle
    return framenum       
  except Exception as inst:
    coordfile.close()
    cam.release()     
    tk.destroy()
    raise inst  
    
    
def play_frame():
  try:
    ret, frame = cam.read()     
    eyes_found, frame = cut_eyes(frame)
    TOC = time.time() - TIC 
    #print(TOC)
    if TOC > MAXTIME: ball.QuitProg(None)
    if(eyes_found):
      position = predict(frame)
      return position      
    else:
      return [round(WIDTH/2) , round(HEIGHT/2)]  #[1,1] # 
  except Exception as inst:
    coordfile.close()
    cam.release()     
    tk.destroy()
    raise inst

#Init output directory and clear it

init_dir(output_dir) # careful! 

#Init parameters of game
#resolution                 
WIDTH = 1600
HEIGHT = 900
BALLSIZE = 40
BALLCOLOR = 'blue'
MAXTIME = 300 #secs, How much time to run the recorder
PLAYMODE = True # Whether to run script in record or play mode
# Init canvas for the ball
tk = Tk()
tk.attributes("-fullscreen", fullscreen)
#tk.wm_attributes('-type', 'splash')
#tk.wm_attributes("-topmost", 0)
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="lightgrey")
canvas.pack()

#Init csv file for ball coordinates 
coordfile = open(output_dir/"coords.csv","w+")
coordfile.write("frame,width,height,time\r\n")

# Init videocapture from camera
cam = cv2.VideoCapture(0)  
TIC = time.time()

#Finally, create ball and start main loop
ball = Ball(canvas)
tk.mainloop()

# free coordfile and camera resources after the loop is finished
coordfile.close()    
cam.release() 





