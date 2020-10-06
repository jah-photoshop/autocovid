#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heirarchical plot for local Covid data - England

Created on Sun Oct  4 14:16:24 2020

@author: jah-photoshop
"""

print("Covid Local Data Plotter - version 1.0   -   @jah-photoshop Oct 2020")
print("")

import os,csv, numpy as np,geopandas as gpd,pandas as pd,matplotlib.pyplot as plt, random, sys
from datetime import datetime, timedelta

debug = True
merge_plots = True
data_path = "data"
output_path = "plots"
output_subpath = output_path + os.path.sep + "maps"
if(os.path.isdir(output_subpath)):
    print("Output path already exists; aborting")
    sys.exit()
else: os.makedirs(output_subpath)
map_filename = "zip://" + data_path + os.path.sep + "Middle_Layer_Super_Output_Areas__December_2011__Boundaries_EW_BSC-shp.zip"
#laa_map_filename = "zip://" + data_path + os.path.sep + "Local_Authority_Districts__May_2020__UK_BUC-shp.zip"

laa_map_filename = "zip://" + data_path + os.path.sep + "Local_Authority_Districts__May_2020__Boundaries_UK_BGC-shp.zip"

town_map_filename = "zip://" + data_path + os.path.sep + "Major_Towns_and_Cities__December_2015__Boundaries-shp.zip"
msoa_filename = data_path + os.path.sep + "MSOAs_latest.csv"
cases_filename = data_path + os.path.sep + "coronavirus-cases_latest.csv"
standalone_plot = False
plot_combined_data = True
post_process = True
plt.rcParams['axes.facecolor']='#121240'
heat_lim = 16
transparent=True
add_overlay=False
add_laa_labels=False

#Yorkshire
frame_margins = [340000,550000,410000,520000]
plot_wales=False
plot_scotland=False
label_x=525000
label_y=510000
l_width=1.2

#England [for combined maps]
frame_margins = [133000,658000,10600,655000]
plot_wales=True
plot_scotland=True
label_x=550000
label_y=576000
l_width=0.6
post_process = True
resize_output = True
heat_lim = 16
transparent = True
add_date = False
add_background = False
target_width = 865
target_height = 1060


#SouthWest
frame_margins = [133000,465000,10600,254000]
plot_wales=True
plot_scotland=False
label_x=170000
label_y=165000
l_width= 3
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 10
transparent = False
add_date = True
add_background = False
target_width = 1280
target_height = 960



#England [for standalone maps]
frame_margins = [133000,658000,10600,655000]
plot_wales=True
plot_scotland=True
plot_towns=True
label_x=550000
label_y=576000
l_width=0.6
post_process = True
resize_output = True
heat_lim = 24
heat_lim = 8
transparent = True
add_date = True
add_background = True
background_file = "heatmap.png"
target_width = 1080
target_height = 1324
mask_colour='#122B49'

plot_laa = True
laa_line_width = 1

#North Yorkshire
frame_margins = [360000,520000,412000,520000]
target_places = ['Craven','Harrogate','Richmondshire','Hambleton','Ryedale','Scarborough','York','Selby']
plot_wales=False
plot_scotland=False
plot_towns=True
plot_laa = True
laa_line_width = 2
label_x=502000
label_y=515000
l_width=1.2
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 8
transparent = False
add_date = True
add_background = False
add_overlay = True
overlay_filename='overlay-nyorks.png'
target_width = 1594
target_height = 1080
#plot_laa_labels=True
laa_fontsize=40
plot_combined_data = True

y_step = (frame_margins[3] - frame_margins[2]) / 2000.0

#Load map data for England [and Wales] from shape file
print("Loading MSOA map data from " + map_filename)
england=gpd.read_file(map_filename,rows=6791)
#wales=gpd.read_file(map_filename,rows=slice(6791,7199)) #Removed; now read wales from LAA file instead for simpler plot...
msoa_names = england.MSOA11CD.to_list()

print("Loading LAA map data from " + laa_map_filename)
england_laa=gpd.read_file(laa_map_filename,rows=314)
laa_centroids = [[c.x,c.y] for c in england_laa.centroid.to_list()]
laa_ids = england_laa.LAD20CD.to_list()
laa_names = england_laa.LAD20NM.to_list()
scotland=gpd.read_file(laa_map_filename,rows=slice(326,357))
wales=gpd.read_file(laa_map_filename,rows=slice(357,379))


print("Loading town map data from ")
towns=gpd.read_file(town_map_filename)
towns['centroids']=towns.centroid
towns=towns.set_geometry('centroids')

#Load MSOA weekly case data from CSV file
print("Loading MSOA data from " + msoa_filename)
with open(msoa_filename) as csv_file: msoa_data = [row for row in csv.reader(csv_file, delimiter=',')][1:-1]

#Load daily case data from CSV file
print("Loading cases data from " + cases_filename)
with open(cases_filename) as csv_file: cases_data = [row for row in csv.reader(csv_file, delimiter=',')][1:-1]
area_codes=list(set([entry[1] for entry in cases_data]))
start_date = datetime(2020, 1, 30)
end_date = datetime.strptime(cases_data[0][3],"%Y-%m-%d")
number_of_days=(end_date-start_date).days + 1
area_codes_index = [e[1] for e in cases_data]
area_rates=[]

#Calculate the case rate, for each day, for each area
print("Calculating area data")
laa_rates = [[0] * number_of_days ] * len(laa_names)
for area_code in area_codes:
    area_cases = [0] * number_of_days
    start_index = area_codes_index.index(area_code)
    area_pop = float(cases_data[start_index][5]) / float(cases_data[start_index][6])
    local_data = [[(datetime.strptime(entry[3],"%Y-%m-%d")-start_date).days,int(entry[4])] for entry in cases_data  if entry[1]==area_code ]
    for line in local_data: area_cases[line[0]]=line[1]  
    area_rate = [( sum(area_cases[max(0,i-6):i+1]) / area_pop) for i in range(number_of_days)]
    if area_code in laa_ids:  
        laa_rates[laa_ids.index(area_code)]=area_rate
        if(debug):print("Area code %s recognised in LAA data (%s), Pop %f  Max rate %f" % (area_code,laa_names[laa_ids.index(area_code)],area_pop,max(area_rate)))
    elif(debug):print("Area code %s not found in LAA data,  Pop %f  Max rate %f" % (area_code,area_pop,max(area_rate)))
    area_rates.append(area_rate)
print("Cross-referencing area data")
ltla_names = [msoa_data[i][4] for i in range(len(msoa_names))]
ltla_indices = []
for name in ltla_names:
    if name in area_codes_index:
        ltla_indices.append(area_codes.index(name))
    else: 
        print("Missing LTLA: %s" % name)
        ltla_indices.append(-1)
        
print("Building msoa history data")
number_of_weeks = int(number_of_days / 7)
day_offsets = [[random.randint(0,6) for i in range(number_of_weeks + 1)] for entry in msoa_data]
hist_msoa_data = []
for count,entry in enumerate(msoa_data):
    adj_msoa = []      
    for day in range(number_of_days):
        day_rate = 0
        if (day > 0): day_rate += adj_msoa[day-1]
        day_rate *= 0.8
        week = int(day / 7)
        if(day % 7 == day_offsets[count][week]): day_rate += ( 0 if int(msoa_data[count][week+8]) < 0 else int(msoa_data[count][week + 8]) )
        if(day_rate < 0.5): day_rate = 0
        adj_msoa.append(day_rate)
    hist_msoa_data.append(adj_msoa)

print("Building map data")
for day in range(number_of_days):
    week=int(day / 7)
    c_date = start_date + timedelta(days=day)
    msoa_series = pd.Series([np.nan if int(row[week+8]) < 0 else int(row[week + 8]) for row in msoa_data])
    msoa_series_title = c_date.strftime('msoa_%m%d')
    england[msoa_series_title]=msoa_series
    ltla_series = pd.Series([np.nan if el < 0 else area_rates[el][day] for el in ltla_indices]) 
    ltla_series_title = c_date.strftime('ltla_%m%d')
    england[ltla_series_title]=ltla_series
    hist_ltla_series = pd.Series([el[day] for el in hist_msoa_data])
    #comb_series = (ltla_series + (6 * hist_ltla_series))**(1/2)
    comb_series = (ltla_series + (6 * hist_ltla_series))**(1/3)
    comb_series_title = c_date.strftime('comb_%m%d')
    england[comb_series_title]=comb_series

print("Producing plots")
def_days = 40  #Plot since 10th March
def_days = 180 #Plot since start of August
#def_days = 30
def_days=210

for day in range(def_days,number_of_days):
    c_date = start_date + timedelta(days=day)
    f_string = output_subpath+os.path.sep+c_date.strftime("map-%Y%m%d.png")
    print("Creating file %s" % (f_string))
    fig,ax = plt.subplots(figsize=(36,36),frameon=not transparent)
    ax.set_aspect('equal')
    ax.axis(frame_margins)
    plt.axis('off')
    if(plot_wales):wales.plot(ax=ax,zorder=1,color=mask_colour)
    if(plot_scotland):scotland.plot(ax=ax,zorder=1,color=mask_colour)

    #england.boundary.plot(ax=ax,zorder=2,linewidth=0.3,color='#888888')
    england.boundary.plot(ax=ax,zorder=2,linewidth=l_width,color='#888888')
    #england.plot(column=c_date.strftime('msoa_%m%d'),ax=ax,cmap='autumn',vmin=3,vmax=30,zorder=4)
    if(plot_combined_data):england.plot(column=c_date.strftime('comb_%m%d'),ax=ax,cmap='YlOrRd',vmin=0,vmax=heat_lim,zorder=3)
    else:  england.plot(column=c_date.strftime('ltla_%m%d'),ax=ax,cmap='OrRd',vmin=0,vmax=200,zorder=3)

    if(plot_laa):england_laa.boundary.plot(ax=ax,zorder=5,linewidth=laa_line_width,color='#553311')
    if(plot_towns):towns.plot(ax=ax,zorder=6,color='#111144')  
    if(plot_laa_labels):
        #laa_centroids.plot(ax=ax,zorder=6,color='#33CC44')
        for name in target_places:
            count=laa_names.index(name)
            val=laa_rates[count][day]
            kx = laa_centroids[count][0]
            ky = laa_centroids[count][1]
            if kx > frame_margins[0] and kx < frame_margins[1] and ky > frame_margins[2] and ky < frame_margins[3]:                
                plt.text(laa_centroids[count][0],laa_centroids[count][1]+(y_step * laa_fontsize),name,horizontalalignment='center',fontsize=laa_fontsize*0.6,bbox=dict(boxstyle='square',color='#AAAA8844'))
                plt.text(laa_centroids[count][0],laa_centroids[count][1]-(y_step * laa_fontsize),"%3.1f" % val,horizontalalignment='center',fontsize=laa_fontsize,bbox=dict(boxstyle='square',color='#FFFFEE11'))
    if add_date: plt.text(label_x,label_y,c_date.strftime("%B %d"), horizontalalignment='center', style='italic',fontsize=60)
    plt.savefig(f_string, bbox_inches='tight')
    if post_process:
        if resize_output: os.system('convert %s -resize %dx%d\! %s' % (f_string,target_width,target_height,f_string))
        if add_background: os.system('composite %s %s %s' % (f_string,background_file,f_string))
        if add_overlay: os.system('composite %s %s %s' % (overlay_filename, f_string,f_string))
    fig.clf()    

