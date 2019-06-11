#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:56:15 2019

@author: Michael Berger
"""


from tkinter import Tk, Canvas
import random as rnd
import time
import cv2
from cut_eyes import cut_eyes, report, clear_dir
from conf import path, fullscreen
 
#import PIL.ImageTk as PI
#import conf.py as GDc


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 50, 50, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        rnd.shuffle(starts)
        self.x = -3 # starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False    
        self.speed = 5
        self.speed_range = [1,7]
        
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False
      
    def randwalk(self,direction):
        return ((self.speed_range[1] - self.speed_range[0]) * rnd.random() + self.speed_range[0]) *direction
      
    def coord(self):
        x = self.canvas.coords(self.id)
        return ','.join(str(int(e)) for e in x[0:2])
      
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        
        if pos[1] <= 0:
            self.y = self.randwalk(self.speed)
        if pos[3] >= self.canvas_height:
            self.y = self.randwalk(-self.speed)  
        if pos[0] <= 0:
            self.x = self.randwalk(self.speed)
        if pos[2] >= self.canvas_width:
            self.x = self.randwalk(-self.speed)
            
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 0, 0, fill=color)
        self.canvas.move(self.id, 0, 0)
        self.x = 0
        self.endProg = False
        self.BeginRec = False
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)    
        self.canvas.bind_all('<Escape>', self.QuitProg )
        self.canvas.bind_all('<s>', self.BeginRecord )
        
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0    
            
    def turn_left(self, evt):
            self.x = -3
    def turn_right(self, evt):
            self.x = 3
    def QuitProg(self, evt):
            #self.canvas.destroy()
            self.endProg = True
    def BeginRecord(self, evt):
            #self.canvas.destroy()
            self.BeginRec = True




def start_game(output_dir):
  # Init canvas for the ball
  resolution = [1600,900]
  tk = Tk()
  tk.title("Bouncing Ball Game")
  tk.attributes("-fullscreen", fullscreen)
  tk.resizable(0, 0)
  #tk.wm_attributes('-type', 'splash')
  tk.wm_attributes("-topmost", 0)
  canvas = Canvas(tk, width=resolution[0], height=resolution[1], bd=0, highlightthickness=0)
  canvas.mainloop
  canvas.pack()
  tk.update()
  paddle = Paddle(canvas, 'blue')
  ball = Ball(canvas, paddle, 'blue')
  paddle.draw()
  
  #Init csv file for coordinates 
  f= open(output_dir/"coords.csv","w+")
  f.write("frame,width,height\r\n")
  
  # Init videocapture from camera
  cam = cv2.VideoCapture(0)  
  framenum = 0
  try:
#    display camera stream before starting recording for face placement. Not working currently
#    while not paddle.BeginRec:     
#      ret, frame = cam.read()
#      im = PI.PhotoImage(image = frame)
#      canvas.create_bitmap(0,0,im, anchor=NW)
#      cut_eyes(frame,show=1)
#      tk.update_idletasks()
#      tk.update()
 
    while not paddle.endProg:
        ret, frame = cam.read()
        if ret==True:
          ball.draw()            
          eyes_found, frame = cut_eyes(frame)
          if(eyes_found):
            cv2.imwrite(str(output_dir/("frame%d.jpg" % framenum)), frame)   #write to  images 'frame№.jpg'
            f.write("%s,%s\r\n" % (framenum, (str(ball.coord()))))  
            framenum = framenum+1  # I intentionally disregard frames that failed to produce an eye region rectangle
        else:
          break            
        tk.update_idletasks()
        tk.update()
        time.sleep(0.005)
  except Exception as inst:
    f.close()
    cam.release()     
    tk.destroy()
    raise inst  
  f.close()    
  cam.release() 
  tk.destroy()

  
output = path/'data/eyetrack_eyes_2'

clear_dir(output) # careful! 
start_game(output)



  #     print(type(inst))    # the exception instance
  #     print(inst.args)     # arguments stored in .args
  #     print(inst)   
   #out.release()    


  # Define the codec and create VideoWriter object
  #fourcc = cv2.VideoWriter_fourcc(*'XVID')
  #out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
  

          #out.write(frame) # write to video file 


