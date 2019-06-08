#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 18:08:46 2019

@author: Michael Berger
"""
import pandas as pd
#import pathlib
import matplotlib.pyplot as plt
from conf import path

coordfile = path/'data/eyetrack_eyes/coords.csv'
coords = pd.read_csv(coordfile, dtype = float)
#coords.head()
plt.plot(coords['x'],coords['y'])
