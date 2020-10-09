#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heirarchical map plot for local Covid data - England

Created on Sun Oct  4 14:16:24 2020

@author: jah-photoshop
"""

print("________________________________________________________________________________")
print("Covid Local Data Map Plotter    -    version 1.1    -    @jah-photoshop Oct 2020")
print("________________________________________________________________________________")


import os,csv, numpy as np,geopandas as gpd,pandas as pd,matplotlib.pyplot as plt, random, sys, time, pickle
from datetime import datetime, timedelta

batch_mode = True
batch_list = ['ltla','msoa','lsoa','default','heatmap','nyorks-lsoa','northeast','northwest','southwest','southeast','midlands','east','yorkshire','northyorkshire']
preset = 'default'

debug = False
overwrite_mode = True           #If set to false, program will halt if output folder exists
data_path = "data"
preset_path = "presets"
output_path = "plots"

if(os.path.isdir(output_path)):
    if not overwrite_mode:
        print("Output path %s already exists; aborting" % (output_path))
        sys.exit()
        
map_filename = "zip://" + data_path + os.path.sep + "Middle_Layer_Super_Output_Areas__December_2011__Boundaries_EW_BSC-shp.zip"
laa_map_filename = "zip://" + data_path + os.path.sep + "Local_Authority_Districts__May_2020__Boundaries_UK_BGC-shp.zip"
lsoa_map_filename = "zip://" + data_path + os.path.sep + "Lower_Layer_Super_Output_Areas__December_2011__Boundaries_EW_BGC_v3-shp.zip"
town_map_filename = "zip://" + data_path + os.path.sep + "Major_Towns_and_Cities__December_2015__Boundaries-shp.zip"
msoa_filename = data_path + os.path.sep + "msoa.csv"
lsoa_filename = data_path + os.path.sep + "lsoa.csv"
cases_filename = data_path + os.path.sep + "casedata.csv"
plt.rcParams['axes.facecolor']='#121240'


if(batch_mode):
    print("RUNNING IN BATCH MODE")
    preset_list = batch_list
else:
    preset_list = [preset]
print("Plots to make: %s" % (preset_list))

def load_parameters(preset_name):
    global short_name,plot_msoa_boundaries,target_places,colour_map,msoa_colour_map,lsoa_colour_map,msoa_alpha,lsoa_alpha,frame_margins,label_x,label_y,title_x,title_y,plot_wales,plot_scotland,plot_towns,plot_laa,title_string,laa_linewidth,standalone_plot,post_process,resize_output,heat_lim,transparent,add_date,add_background,add_overlay,add_title,target_width,target_height,plot_laa_names,plot_laa_values,plot_ltla_data,plot_msoa_data,plot_lsoa_data,plot_combined_data,text_align_mode,date_font_size,title_font_size,laa_fontsize,mask_colour,add_footer,restrict_laa_to_targets,f_scale,overlay_filename,background_file
    with open(preset_path + os.path.sep + preset_name + ".pickle","rb") as f: preset_data=pickle.load(f)        
    short_name,plot_msoa_boundaries,target_places,colour_map,msoa_colour_map,lsoa_colour_map,msoa_alpha,lsoa_alpha,frame_margins,label_x,label_y,title_x,title_y,plot_wales,plot_scotland,plot_towns,plot_laa,title_string,laa_linewidth,standalone_plot,post_process,resize_output,heat_lim,transparent,add_date,add_background,add_overlay,add_title,target_width,target_height,plot_laa_names,plot_laa_values,plot_ltla_data,plot_msoa_data,plot_lsoa_data,plot_combined_data,text_align_mode,date_font_size,title_font_size,laa_fontsize,mask_colour,add_footer,restrict_laa_to_targets,f_scale,overlay_filename,background_file = preset_data

using_lsoa_data = False

for plot in preset_list:
    load_parameters(plot)
    if plot_lsoa_data: using_lsoa_data = True


y_step = (frame_margins[3] - frame_margins[2]) / 2000.0

print("________________________________________________________________________________")
print("LOADING MAP DATA")
#Load map data for England [and Wales] from shape file
print("Loading MSOA map data from " + map_filename)
england=gpd.read_file(map_filename,rows=6791)
#wales=gpd.read_file(map_filename,rows=slice(6791,7199)) #Removed; now read wales from LAA file instead for simpler plot...
msoa_names = england.MSOA11CD.to_list()

#Load LSOA map data for England [and Wales] from shape file
if(using_lsoa_data):
    print("Loading LSOA map data from " + lsoa_map_filename)
    lsoa_map=gpd.read_file(lsoa_map_filename,rows=32844)
else: print("Not loading LSOA data")

print("Loading LAA map data from " + laa_map_filename)
england_laa=gpd.read_file(laa_map_filename,rows=314)
laa_centroids = [[c.x,c.y] for c in england_laa.centroid.to_list()]
laa_ids = england_laa.LAD20CD.to_list()
laa_names = england_laa.LAD20NM.to_list()
scotland=gpd.read_file(laa_map_filename,rows=slice(326,357))
wales=gpd.read_file(laa_map_filename,rows=slice(357,379))

print("Loading town map data from " + town_map_filename)
towns=gpd.read_file(town_map_filename)
towns['centroids']=towns.centroid
towns=towns.set_geometry('centroids')

print("________________________________________________________________________________")
print("LOADING CASE DATA")
#Load MSOA weekly case data from CSV file
print("Loading MSOA data from " + msoa_filename)
with open(msoa_filename) as csv_file: msoa_data = [row for row in csv.reader(csv_file, delimiter=',')][1:-1]

#Load LSOA weekly case data from CSV file
if(using_lsoa_data):
    print("Loading LSOA data from " + lsoa_filename)
    with open(lsoa_filename) as csv_file: raw_lsoa_data= [row for row in csv.reader(csv_file, delimiter=',')][1:-1]

#Load daily case data from CSV file
print("Loading cases data from " + cases_filename)
with open(cases_filename) as csv_file: cases_data = [row for row in csv.reader(csv_file, delimiter=',')][1:-1]
area_codes=list(set([entry[1] for entry in cases_data]))
start_date = datetime(2020, 1, 30)
end_date = datetime.strptime(cases_data[0][3],"%Y-%m-%d")
number_of_days=(end_date-start_date).days + 1
area_codes_index = [e[1] for e in cases_data]
area_rates=[]
file_date=datetime.strptime(time.ctime(os.path.getctime(cases_filename)),"%c")
file_age=(datetime.today()-file_date).days
if file_age > 0 : print ("Warning: The cases file is %d days old..." % (file_age))


print("________________________________________________________________________________")
print("PROCESSING DATA")        
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
        if debug: print("Missing LTLA: %s" % name)
        ltla_indices.append(-1)

if(using_lsoa_data):
    print ("Cross-referencing LSOA data")
    lsoa_map_cd_list = lsoa_map.LSOA11CD.to_list()
    lsoa_data_cd_list = [e[0] for e in raw_lsoa_data]
    lsoa_xref_list = []
    lsoa_data = []
    w_l = len(raw_lsoa_data[0])
    for count,entry in enumerate(lsoa_map_cd_list):
        if entry not in lsoa_data_cd_list:
            if(debug):print("LSOA %s not found in data set" % (entry))
            lsoa_xref_list.append(-1)
            lsoa_data.append([[-99] * w_l])
        else: 
            ix = lsoa_data_cd_list.index(entry)
            lsoa_xref_list.append(ix)
            lsoa_data.append(raw_lsoa_data[ix])
    
print("Building MSOA history data")
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
    

if(using_lsoa_data):
    print("Building LSOA history data")
    lsoa_day_offsets = [[random.randint(0,6) for i in range(number_of_weeks + 1)] for entry in lsoa_data]
    hist_lsoa_data = []
    lsoa_warning = False
    for count,entry in enumerate(lsoa_data):
        adj_lsoa = []      
        #Fill out data set with zeros if not up to date with cases data
        while( int(number_of_days / 7) + 2 >= len(entry) ):
            if not lsoa_warning: print ("Warning: No LSOA data for week %d" % (len(entry) - 8))     
            lsoa_warning = True
            entry.append(-99)
        for day in range(number_of_days):
            day_rate = 0
            if (day > 0): day_rate += adj_lsoa[day-1]
            day_rate *= 0.8
            week = int(day / 7)
            if(day % 7 == lsoa_day_offsets[count][week]): day_rate += ( 0 if int(lsoa_data[count][week+2]) < 0 else int(lsoa_data[count][week + 2]) )
            if(day_rate < 0.5): day_rate = 0
            adj_lsoa.append(day_rate)
        hist_lsoa_data.append(adj_lsoa)


print("Building map data")
for day in range(number_of_days):
    week=int(day / 7)
    c_date = start_date + timedelta(days=day)
    msoa_series = pd.Series([np.nan if int(row[week+8]) < 0 else int(row[week + 8]) for row in msoa_data])
    msoa_series_title = c_date.strftime('msoa_%m%d')
    england[msoa_series_title]=msoa_series
    if(using_lsoa_data):
        lsoa_series = pd.Series([np.nan if int(row[week+2]) < 0 else int(row[week + 2]) for row in lsoa_data])
        lsoa_series_title = c_date.strftime('lsoa_%m%d')
        lsoa_map[lsoa_series_title]=lsoa_series
    ltla_series = pd.Series([np.nan if el < 0 else area_rates[el][day] for el in ltla_indices]) 
    ltla_series_title = c_date.strftime('ltla_%m%d')
    england[ltla_series_title]=ltla_series
    hist_ltla_series = pd.Series([el[day] for el in hist_msoa_data])
    #comb_series = (ltla_series + (6 * hist_ltla_series))**(1/2)
    comb_series = (ltla_series + (6 * hist_ltla_series))**(1/3)
    comb_series_title = c_date.strftime('comb_%m%d')
    england[comb_series_title]=comb_series

print("________________________________________________________________________________")
print("PRODUCING PLOTS")
def_days = 30  #Plot since 1st March
#def_days = 180 #Plot since start of August
def_days = 31
#def_days=250
print("Plotting %d days of data [%s to %s]" % (number_of_days-def_days, (start_date + timedelta(days=def_days)).strftime("%d/%m/%Y"), (start_date + timedelta(days=number_of_days - 1)).strftime("%d/%m/%Y") ))
print("________________________________________________________________________________")

#fig,ax = plt.subplots(figsize=(36,36),frameon=not transparent)
#fig=plt.figure(figsize=(36,36),frameon=not transparent)
for pre in preset_list:
        
    #Load plot parameters from pickle file
    print("Plotting maps for preset " + pre)
    load_parameters(pre)
    fig=plt.figure(figsize=(36,36),frameon=not transparent)
    output_subpath = output_path + os.path.sep + short_name
    #print("Output subpath %s" % output_subpath)
    if not os.path.exists(output_subpath): os.makedirs(output_subpath)
    if not restrict_laa_to_targets: target_places=list(set([entry[0] for entry in cases_data]))
    for target in list.copy(target_places):
        if target not in laa_names:
            if debug: print("Target %s is not in LTLA list" % (target))
            target_places.remove(target) 
    for day in range(def_days,number_of_days):
        c_date = start_date + timedelta(days=day)
        f_string = output_subpath+os.path.sep+c_date.strftime("map-%Y%m%d.png")
        print("Creating file %s" % (f_string))
        ax=plt.gca()
        ax.set_aspect('equal')
        ax.axis(frame_margins)
        
        #divider = make_axes_locatable(ax)
        #cax = divider.append_axes("bottom",size="5%",pad=0.1)
        plt.axis('off')
        z=0
        if(plot_wales):
            wales.plot(ax=ax,zorder=z,color=mask_colour)
            z+=1
        if(plot_scotland):
            scotland.plot(ax=ax,zorder=z,color=mask_colour)
            z+=1
        if(plot_msoa_boundaries):
            england.boundary.plot(ax=ax,zorder=z,linewidth=laa_linewidth,color='#888888')
            z+=1
        if(plot_ltla_data):
            england.plot(column=c_date.strftime('ltla_%m%d'),ax=ax,cmap=colour_map,vmin=0,vmax=200,zorder=z)
            z+=1
        if(plot_combined_data):
            england.plot(column=c_date.strftime('comb_%m%d'),ax=ax,cmap=colour_map,vmin=0,vmax=heat_lim,zorder=z)
            z+=1
        if(plot_msoa_data):
            england.plot(column=c_date.strftime('msoa_%m%d'),ax=ax,cmap=msoa_colour_map,vmin=3,vmax=30,zorder=z,alpha=msoa_alpha)
            z+=1
        if(plot_lsoa_data):
            lsoa_map.plot(column=c_date.strftime('lsoa_%m%d'),ax=ax,cmap=lsoa_colour_map,vmin=3,vmax=30,zorder=z,alpha=lsoa_alpha)
            z+=1
        if(plot_laa):
            england_laa.boundary.plot(ax=ax,zorder=z,linewidth=laa_linewidth,color='#553311')
            z+=1
        if(plot_towns):
            towns.plot(ax=ax,zorder=z,color='#111144')
            z+=1
        if(plot_laa_names or plot_laa_values):
            #laa_centroids.plot(ax=ax,zorder=6,color='#33CC44')
            for name in target_places:
                count=laa_names.index(name)
                val=laa_rates[count][day]
                kx = laa_centroids[count][0]
                ky = laa_centroids[count][1]
                if kx > frame_margins[0] and kx < frame_margins[1] and ky > frame_margins[2] and ky < frame_margins[3]:                
                    #Plot labels text centered unless within 10% of RHS or LHS margin
                    al_mode = 'center'
                    if kx > ( (frame_margins[1] - frame_margins[0]) * 0.95) + frame_margins[0]: al_mode = 'right'
                    if kx < ( (frame_margins[1] - frame_margins[0]) * 0.05) + frame_margins[0]: al_mode = 'left'
                    y_shift = 0
                    if ky > ( (frame_margins[3] - frame_margins[2]) * 0.95) + frame_margins[2]: y_shift = -2 * (y_step * laa_fontsize)
                    if ky < ( (frame_margins[3] - frame_margins[2]) * 0.05) + frame_margins[2]: y_shift = 2 * (y_step * laa_fontsize)
                    yy_shift = 0
                    if plot_laa_names: 
                        yy_shift = y_step * laa_fontsize
                        plt.text(laa_centroids[count][0],laa_centroids[count][1]+y_shift+yy_shift,name,horizontalalignment=al_mode,fontsize=laa_fontsize*0.6,bbox=dict(boxstyle='square',color='#AAAA8877'))
                    if plot_laa_values: plt.text(laa_centroids[count][0],laa_centroids[count][1]+y_shift-yy_shift,"%3.1f" % val,horizontalalignment=al_mode,fontsize=laa_fontsize,bbox=dict(boxstyle='square',color='#FFFFEE11'))
        if add_date: plt.text(label_x,label_y,c_date.strftime("%B %d"), horizontalalignment=text_align_mode, style='italic',fontsize=date_font_size)
        if add_title:plt.text(title_x,title_y,title_string,horizontalalignment=text_align_mode,fontsize=title_font_size)
        if add_footer:    
            footer = file_date.strftime("Based on LTLA and MSOA case data from coronavirus.data.gov.uk, data set published %d/%m/%y. github.com/jah-photoshop/autocovid")
            fr_scale = f_scale
            if(plot_laa_values): 
                footer = "Values are cases/100K/week. "+footer
                fr_scale = f_scale * 1.2
            plt.text(frame_margins[1]-( (frame_margins[1] - frame_margins[0]) * 0.01),frame_margins[2]+( (frame_margins[3] - frame_margins[2]) * 0.01),footer,horizontalalignment='right',fontsize=title_font_size / fr_scale, bbox=dict(boxstyle='square',color='#AAAA8844'))
        plt.savefig(f_string, bbox_inches='tight')
        if post_process:
            if resize_output: os.system('convert %s -resize %dx%d\! %s' % (f_string,target_width,target_height,f_string))
            if add_background: os.system('composite %s %s %s' % (f_string,background_file,f_string))
            if add_overlay: os.system('composite %s %s %s' % (overlay_filename, f_string,f_string))
        fig.clf()    
    print("________________________________________________________________________________")
print("Operation complete.")
