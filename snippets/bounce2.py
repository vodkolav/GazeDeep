#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 11:56:15 2019

@author: michael
"""

from tkinter import Tk, Canvas
import random as rnd
import time
import numpy as np

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
      
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        print(np.round(pos))
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
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)    
        self.canvas.bind_all('<Escape>', self.QuitProg )
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
            self.canvas.destroy()
            self.endProg = True
  
            
tk = Tk()
tk.title("Bouncing Ball Game")
tk.attributes("-fullscreen", False)
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 0)
canvas = Canvas(tk, width=1800, height=900, bd=0, highlightthickness=0)
canvas.mainloop
canvas.pack()
tk.update()
paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'blue')
paddle.draw()
while 1:
    if  not paddle.endProg:
      ball.draw()    
    else:
      break
    tk.update_idletasks()
    tk.update()
    time.sleep(0.03)
tk.destroy()
