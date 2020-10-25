#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fancy_video.py

Script to add extra frames to video

Created on Fri Oct 23 13:15:57 2020

@author: jah-photoshop
"""

import os, glob

target_folder = "plots/doubling-bin"
output_folder = target_folder + os.path.sep + "fancy"

s_frames = glob.glob(target_folder + os.path.sep + "*.png")
s_frames.sort()

if not os.path.exists(output_folder): os.mkdir(output_folder)

hold_frames = 2
for fcount, frame in enumerate(s_frames[:-2]):
    name = os.path.splitext(os.path.basename(frame))[0]
    count = 0
    ofs_name = output_folder + os.path.sep + name
    next_frame = s_frames[fcount+1]
    for i in range(hold_frames):
        cp_line="cp " + frame + " " + ofs_name + ("_%02d.png" % count)
        os.system(cp_line)
        count+=1    
    mf_line = "composite -dissolve 94 -gravity Center " + frame + " " + next_frame + " -alpha Set " + ofs_name + ("_%02d.png" % (count + 0))
    mf2_line = "composite -dissolve 82 -gravity Center " + frame + " " + next_frame + " -alpha Set " + ofs_name + ("_%02d.png" % (count + 1))
    mf3_line = "composite -dissolve 58 -gravity Center " + frame + " " + next_frame + " -alpha Set " + ofs_name + ("_%02d.png" % (count + 2))
    mf4_line = "composite -dissolve 16 -gravity Center " + frame + " " + next_frame + " -alpha Set " + ofs_name + ("_%02d.png" % (count + 3))
    os.system(mf_line)
    os.system(mf2_line)
    os.system(mf3_line)
    os.system(mf4_line)

    
    
        
        