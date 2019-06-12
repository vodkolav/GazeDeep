#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:08:46 2019

@author: Michael Berger
"""
import pandas as pd
#import pathlib
import matplotlib.pyplot as plt
from sys import stdout
from conf import output_dir

coordfile = output_dir/'coords.csv'
coords = pd.read_csv(str(coordfile), dtype = float)


def report(what):
  """
  like print() but reports on the same line so that output doesn't end up cluttered
  """
  stdout.write("\r%s" % what)
  stdout.flush()


def init_dir(path):
  if not path.exists():
    path.mkdir()
    return
  from conf import force_clear 
  nfiles = len([file for file in path.iterdir() if file.is_file()])
  if nfiles < 300 or force_clear:      
    for fl in path.iterdir():
      if fl.suffix == '.jpg':
        report('removing file ' + fl.name)    
        fl.unlink()
  else:
    print("If you want to remove more than 300 files, you must set conf.force_clear to True first!")
    #cut_eyes(str(fl), dest_path= str(dest_dir_path/fl.name))
  


def plot_ball_trajectory(coords):
  #coords.head()
  plt.plot(coords['width'],coords['height'], 'o', markersize=2)



def frames_per_second_graph(coords):
  #coords = pd.read_csv(str(coordfile), delimiter = ',')
  coords['time'] = round(coords['time'])
  cnt = coords.groupby('time').count()
  plt.plot(cnt['frame'], 'o', markersize=2)


plot_ball_trajectory(coords)
#frames_per_second_graph(coordfile)


w = coords['width']
h = coords['height']
plt.hist(h, bins= 100  )




