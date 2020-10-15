#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 10:25:32 2020

@author: robotlab
"""

import glob, os, shutil
from datetime import datetime, timedelta

start_date = datetime(2020,3,1)
end_date = datetime(2020,10,6)
framerate = 4
holdtime = 1

def get_date(filename):
    return datetime.strptime(os.path.splitext(os.path.basename(filename))[0],"map-%Y%m%d")


plots_path = "30day/output-20201009"
output_path = "videos"
if not os.path.exists(output_path): os.mkdir(output_path)
subfolders = glob.glob(plots_path + os.path.sep + "*")
for folder in subfolders:
    print ("Creating video file for %s" % folder)
    map_files = glob.glob(folder + os.path.sep + "*.png")
    map_files.sort()
    trim_map_files = [mf for mf in map_files if get_date(mf) <= end_date and get_date(mf) >= start_date]
    if os.path.exists(folder+os.path.sep+"temp"): shutil.rmtree(folder+os.path.sep+"temp")    
    os.mkdir(folder + os.path.sep + "temp")
    for mf in trim_map_files: shutil.copyfile(mf,folder+os.path.sep+"temp"+os.path.sep+os.path.basename(mf))
    for rf in range(int(holdtime * framerate)): shutil.copyfile(trim_map_files[-1],folder+os.path.sep+"temp"+os.path.sep+os.path.splitext(os.path.basename(trim_map_files[-1]))[0]+("-%02d.png" % rf)) 
    ffmpeg_line = ("ffmpeg -framerate %d -pattern_type glob -i '" % (framerate)) + folder + os.path.sep+ "temp" + os.path.sep + "*.png' -c:v libx264 -r 30 -pix_fmt yuv420p "+output_path+os.path.sep+os.path.basename(folder)+".mp4"
    os.system(ffmpeg_line)
    shutil.rmtree(folder+os.path.sep+"temp")    

#
#lsoa_path = "plots/lsoa"
#
##background_files = glob.glob(background_path + os.path.sep + "*.png")
#lsoa_files = glob.glob(lsoa_path + os.path.sep + "*.png")
#background_files.sort()
#lsoa_files.sort()
#
##print(background_files)
##print(lsoa_files)
#
#background_dates = [datetime.strptime(os.path.splitext(os.path.basename(file))[0],"%Y%m%d") for file in background_files]
#print (datetime.strftime(background_dates[0],"Oldest background image: %d %b"))
#print (datetime.strftime(background_dates[-1],"Newest background image: %d %b"))
#
#oldest_lsoa_s=os.path.basename(lsoa_files[0])[:8]
#newest_lsoa_s=os.path.basename(lsoa_files[-1])
##[0][:8]
##print(oldest_lsoa_s)
##print(newest_lsoa_s)
#
#oldest_lsoa = datetime.strptime(oldest_lsoa_s,"%Y%m%d")
#newest_lsoa = datetime.strptime(newest_lsoa_s[:8],"%Y%m%d")
#frames_per_day = int(newest_lsoa_s[9:12]) + 1
#print (datetime.strftime(oldest_lsoa,"Oldest LSOA image      : %d %b"))
#print (datetime.strftime(newest_lsoa,"Newest LSOA image      : %d %b"))
#
#print ("Frames per day         : %d" % frames_per_day)
#number_of_days = (background_dates[-1]-background_dates[0]).days + 1
#number_of_frames = number_of_days * frames_per_day
#print ("Number of days         : %d" % number_of_days)
#date_offset = (oldest_lsoa - background_dates[0]).days
#print ("LSOA date offset       : %d" % date_offset)
#print ("Number of frames       : %d" % number_of_frames)
#print
#for frame in range(number_of_frames):
#    rel_day = int(frame / frames_per_day)
#    rel_date = background_dates[0] + timedelta(days=rel_day)
#    
#    frame_name = "%05d" % frame
#    print("\rCreating frame %s " % (frame_name))
#    filename = "output" + os.path.sep + frame_name + ".png"
#    lsoa_index = frame - (date_offset * frames_per_day)
#    
#    #Check if LSOA data exists for frame
#    if(rel_date >= oldest_lsoa and lsoa_index < len(lsoa_files)):
#        #Create combined image
#        os.system('composite -geometry +980+20 %s %s %s' % (lsoa_files[lsoa_index],background_files[rel_day],filename))
#    else:
#        #If LSOA data doesn't exist just duplicate background
#        os.system('cp %s %s' % (background_files[rel_day],filename))
