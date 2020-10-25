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


import os,csv, numpy as np,geopandas as gpd,pandas as pd,scipy.stats as ss, matplotlib.pyplot as plt, random, sys, time, pickle, shutil, mapclassify as mc
from datetime import datetime, timedelta
from math import log

#def_days = 31  #Plot since 1st March
#def_days = 180 #Plot since start of August
def_days = 31
#def_days=100
#def_dayage

batch_mode = True
batch_list = ['ltla','msoa','lsoa','default','rank','london','heatmap','nyorks-lsoa','northeast','northwest','southwest','southeast','midlands','east','yorkshire','northyorkshire']

batch_list=['london-phe','london-phex','ltla-phe','ltla-phex']
batch_list=['nyorks-bin']
batch_list=['age-risk','age-risk-unweighted']
batch_list=['norfolk']
batch_list =['doubling-bin']
batch_list=['doubling-bin']
batch_list=['msoa']


batch_list=['doubling-london','doubling-bin']
batch_list=['rank']
#preset='doubling-'
debug = False
overwrite_mode = True           #If set to false, program will halt if output folder exists
archive = False
data_path = "data"
preset_path = "presets"
output_path = "plots"
archive_path = datetime.now().strftime("/home/robotlab/jah-photoshop-googledrive/output-%Y%m%d/")
preset = 'default'

#ltla_vmax=200

if(os.path.isdir(output_path)):
    if not overwrite_mode:
        print("Output path %s already exists; aborting" % (output_path))
        sys.exit()
        
map_filename = "zip://" + data_path + os.path.sep + "Middle_Layer_Super_Output_Areas__December_2011__Boundaries_EW_BSC-shp.zip"
laa_map_filename = "zip://" + data_path + os.path.sep + "Local_Authority_Districts__May_2020__Boundaries_UK_BGC-shp.zip"
lsoa_map_filename = "zip://" + data_path + os.path.sep + "Lower_Layer_Super_Output_Areas__December_2011__Boundaries_EW_BGC_v3-shp.zip"
town_map_filename = "zip://" + data_path + os.path.sep + "Major_Towns_and_Cities__December_2015__Boundaries-shp.zip"
electoral_map_filename = "zip://" + data_path + os.path.sep + "Westminster_Parliamentary_Constituencies__December_2019__Boundaries_UK_BGC-shp.zip"

msoa_filename = data_path + os.path.sep + "msoa.csv"
lsoa_filename = data_path + os.path.sep + "lsoa.csv"
cases_filename = data_path + os.path.sep + "casedata.csv"
laa_risk_filename = data_path + os.path.sep + "age_risk_index.csv"
plt.rcParams['axes.facecolor']='#121240'

plot_electoral_boundaries = False

const_list = ['Broadland','North Norfolk','North West Norfolk','Mid Norfolk','Norwich North','Sleaford and North Hykeham',
              'North Herefordshire','Ashford','Dudley North','Devizes','North Cornwall','Central Suffolk and North Ipswich',
              'Ipswich','South Cambridgeshire','North Devon','Truto and Falmouth','Yeovil','South East Cornwall',
              'Newton Abbot','St Austell and Newquay'] 
const_names = [['Jerome','Mayhew'],['Duncan','Baker'],['James','Wild'],['George','Freeman'],['Chloe','Smith'],['Caroline','Johnson'],
               ['Bill','Wiggin'],['Damian','Green'],['Marco','Longhi'],['Danny','Kruger'],['Scott','Mann'],['Dan','Poulter'],
               ['Tom','Hunt'],['Anthony','Browne'],['Selaine','Saxby'],['Cherilyn','Mackrory'],['Marcus','Fysh'],['Sheryl','Murray'],
               ['Anne-Marie','Morris'],['Steve','Double']
            ] 
if(batch_mode):
    print("RUNNING IN BATCH MODE")
    preset_list = batch_list
else:
    preset_list = [preset]
print("Plots to make: %s" % (preset_list))

def load_parameters(preset_name):
    global short_name,sqrt_rates,plot_risk_weighted_ltla,plot_risk_weighted_ltla_binned,ltla_vmax,plot_classified_ltla,ltla_classifier_mode,ltla_classifier_bins,footer_message,plot_ranks,plot_relative,relative_days,plot_msoa_boundaries,target_places,colour_map,msoa_colour_map,lsoa_colour_map,msoa_alpha,lsoa_alpha,frame_margins,label_x,label_y,title_x,title_y,plot_wales,plot_scotland,plot_towns,plot_laa,title_string,laa_linewidth,standalone_plot,post_process,resize_output,heat_lim,transparent,add_date,add_background,add_overlay,add_title,target_width,target_height,plot_laa_names,plot_laa_values,plot_ltla_data,plot_msoa_data,plot_lsoa_data,plot_combined_data,text_align_mode,date_font_size,title_font_size,laa_fontsize,mask_colour,add_footer,restrict_laa_to_targets,f_scale,overlay_filenames,overlay_positions,background_file
    with open(preset_path + os.path.sep + preset_name + ".pickle","rb") as f: preset_data=pickle.load(f)        
    short_name,sqrt_rates,plot_risk_weighted_ltla,plot_risk_weighted_ltla_binned,ltla_vmax,plot_classified_ltla,ltla_classifier_mode,ltla_classifier_bins,footer_message,plot_ranks,plot_relative,relative_days,plot_msoa_boundaries,target_places,colour_map,msoa_colour_map,lsoa_colour_map,msoa_alpha,lsoa_alpha,frame_margins,label_x,label_y,title_x,title_y,plot_wales,plot_scotland,plot_towns,plot_laa,title_string,laa_linewidth,standalone_plot,post_process,resize_output,heat_lim,transparent,add_date,add_background,add_overlay,add_title,target_width,target_height,plot_laa_names,plot_laa_values,plot_ltla_data,plot_msoa_data,plot_lsoa_data,plot_combined_data,text_align_mode,date_font_size,title_font_size,laa_fontsize,mask_colour,add_footer,restrict_laa_to_targets,f_scale,overlay_filenames,overlay_positions,background_file = preset_data

using_lsoa_data = False
use_manual_binning = False
risk_weighted = False

for plot in preset_list:
    load_parameters(plot)
    if plot_lsoa_data: using_lsoa_data = True
    if plot_risk_weighted_ltla: risk_weighted = True 
    if plot_classified_ltla:
        if ltla_classifier_mode == 'manual':
            use_manual_binning = True


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

if(plot_electoral_boundaries):
    print("Loading electoral map data from " + electoral_map_filename)
    all_constituencies = gpd.read_file(electoral_map_filename)
    constituencies = all_constituencies.loc[all_constituencies['pcon19nm'].isin(const_list)]

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
area_ranks=[]
file_date=datetime.strptime(time.ctime(os.path.getctime(cases_filename)),"%c")
file_age=(datetime.today()-file_date).days
if file_age > 0 : print ("Warning: The cases file is %d days old..." % (file_age))

if(risk_weighted):
    print("Loading risk weightings from " + laa_risk_filename)
    with open(laa_risk_filename) as risk_file: weightings_data = [row for row in csv.reader(risk_file, delimiter=',')]
    rw_indices = [w[0] for w in weightings_data]
    rw_values = [float(w[2]) for w in weightings_data]
    area_weights = []
    for ac in area_codes:
            if ac not in rw_indices:
                print("Warning: %s not found in weightings data" % ac)
            #    area_weights.append(0.0) #replace with 1.0
            #else: area_weights.append(log(rw_values[rw_indices.index(ac)],2)) #remove log
                area_weights.append(1.0) #replace with 1.0
            else: area_weights.append(rw_values[rw_indices.index(ac)]) #remove log
        

print("________________________________________________________________________________")
print("PROCESSING DATA")        
#Calculate the case rate, for each day, for each area
print("Calculating area data")
laa_rates = [[0] * number_of_days ] * len(laa_names)
relative_area_rates = []  #Store change in rates over 7 day period
weighted_area_rates = []

for ac, area_code in enumerate(area_codes):
    area_cases = [0] * number_of_days
    start_index = area_codes_index.index(area_code)
    area_pop = float(cases_data[start_index][5]) / float(cases_data[start_index][6])
    local_data = [[(datetime.strptime(entry[3],"%Y-%m-%d")-start_date).days,int(entry[4])] for entry in cases_data  if entry[1]==area_code ]
    for line in local_data: area_cases[line[0]]=line[1]  
    area_rate = [( sum(area_cases[max(0,i-6):i+1]) / area_pop) for i in range(number_of_days)]
    relative_area_rate = []
    for i in range(number_of_days):
        if(i<relative_days): relative_area_rate.append(0)
        else:
            h_area_rate = area_rate[i-relative_days]
            if h_area_rate == 0: relative_area_rate.append(0)
            else:
                z = area_rate[i]/h_area_rate
                if(z == 0):relative_area_rate.append(0)
                else: relative_area_rate.append(log(z,2))
    relative_area_rates.append(relative_area_rate)
    if area_code in laa_ids:  
        laa_rates[laa_ids.index(area_code)]=area_rate
        if(debug):print("Area code %s recognised in LAA data (%s), Pop %f  Max rate %f" % (area_code,laa_names[laa_ids.index(area_code)],area_pop,max(area_rate)))
    elif(debug):print("Area code %s not found in LAA data,  Pop %f  Max rate %f" % (area_code,area_pop,max(area_rate)))
    area_rates.append(area_rate)
    if(risk_weighted):
        weighted_area_rate = [r * area_weights[ac] for r in area_rate]
        weighted_area_rates.append(weighted_area_rate)
calc_ltla_rank = True    
if(calc_ltla_rank):
    print("Calculating area ranks")
    for day in range(number_of_days):
        rates = [area[day] for area in area_rates]
        ranked = ss.rankdata(rates) / len(area_rates)
        area_ranks.append(ranked)
        
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
    if sqrt_rates: ltla_series = ltla_series.pow(0.5)
    ltla_series_title = c_date.strftime('ltla_%m%d')
    england[ltla_series_title]=ltla_series
    hist_ltla_series = pd.Series([el[day] for el in hist_msoa_data])    
    #comb_series = (ltla_series + (6 * hist_ltla_series))**(1/2)
    comb_series = (ltla_series + (6 * hist_ltla_series))**(1/3)
    comb_series_title = c_date.strftime('comb_%m%d')
    england[comb_series_title]=comb_series
    if(calc_ltla_rank):
        ltla_rank_series = pd.Series([area_ranks[day][el] for el in ltla_indices])
        ltla_rank_series_title = c_date.strftime('rank_%m%d')
        england[ltla_rank_series_title]=ltla_rank_series
    ltla_relative_series = pd.Series([relative_area_rates[el][day] for el in ltla_indices])
    ltla_relative_series_title = c_date.strftime('relative_%m%d')
    england[ltla_relative_series_title]=ltla_relative_series
    if(risk_weighted):
        #ltla_risk_series = pd.Series([area_weights[el] for el in ltla_indices])
        ltla_risk_series = pd.Series([weighted_area_rates[el][day] for el in ltla_indices])
        if sqrt_rates: ltla_risk_series = ltla_risk_series.pow(0.5)
        ltla_risk_series_title = c_date.strftime('risk_%m%d')
        england[ltla_risk_series_title]=ltla_risk_series
    
    if(use_manual_binning):
        b_val = -0.1
        bin_totals=[]
        rw_bin_totals=[]
        for el in ltla_indices:
            bin_count = 0
            w_bin_count = 0
            for bin_val in ltla_classifier_bins:
                if area_rates[el][day] > bin_val: bin_count += 1
                if risk_weighted and weighted_area_rates[el][day] > bin_val: w_bin_count += 1
            bin_totals.append(bin_count)
            if risk_weighted: rw_bin_totals.append(w_bin_count)
        england[c_date.strftime('bin_%m%d')]=pd.Series(bin_totals)
        if risk_weighted: england[c_date.strftime('rwbin_%m%d')]=pd.Series(rw_bin_totals)
#        for count,cbin in enumerate(ltla_classifier_bins):
#            bin_series_title=('bin%02d' % count) + c_date.strftime('%m%d')
#            bin_series = pd.Series([np.nan if area_rates[el][day] < b_val or area_rates[el][day]>=cbin else 1 for el in ltla_indices])
#            b_val = cbin
#            england[bin_series_title]=bin_series
#            
print("________________________________________________________________________________")
print("PRODUCING PLOTS")

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
    y_step = (frame_margins[3] - frame_margins[2]) / 2000.0

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
            england.plot(column=c_date.strftime('ltla_%m%d'),ax=ax,cmap=colour_map,vmin=0,vmax=ltla_vmax,zorder=z)
            z+=1
        if(plot_classified_ltla):
            if ltla_classifier_mode == 'manual':
                england.plot(column=c_date.strftime('bin_%m%d'),ax=ax,vmin=0,vmax=len(ltla_classifier_bins)-1,cmap=colour_map,zorder=z)
                z+=1
#                ltla_classifier_colours = ['#338ed7','#ddfffe','#d9fedf','#f3ff92','#ffa923','#e90418','#ad0620']
#                for count,cbin in enumerate(ltla_classifier_bins):
#                    england.plot(column=('bin%02d' % count) + c_date.strftime('%m%d'),ax=ax,vmin=0,vmax=1,facecolor=ltla_classifier_colours[count],zorder=z)
#                    z+=1
            else:
                #Classify the relevant data using mapclassify
                classified = mc.UserDefined(england.get(c_date.strftime('ltla_%m%d')),ltla_classifier_bins)
                classified.plot(england,ax=ax,cmap=colour_map,border_width=0.1,border_color='#EEEEEE22',legend=True,legend_kwds={'loc':'center left'})            
        if(plot_risk_weighted_ltla_binned):
                england.plot(column=c_date.strftime('rwbin_%m%d'),ax=ax,vmin=0,vmax=len(ltla_classifier_bins)-1,cmap=colour_map,zorder=z)
                z+=1
        if(plot_ranks):
#            england.plot(column=c_date.strftime('rank_%m%d'),ax=ax,cmap=colour_map,vmin=0.0,vmax=1.0,zorder=z)
            #q_scheme=mc.Quantiles(england.get(c_date.strftime('rank_%m%d')),k=4)
            #england.plot(column=c_date.strftime('rank_%m%d'),ax=ax,cmap=colour_map,zorder=z,scheme='quantiles')#vmin=0.0,vmax=1.0,
            england.plot(column=c_date.strftime('rank_%m%d'),ax=ax,cmap=colour_map,zorder=z,vmin=0.0,vmax=1.0)
            z+=1
        if(plot_combined_data):
            england.plot(column=c_date.strftime('comb_%m%d'),ax=ax,cmap=colour_map,vmin=0,vmax=heat_lim,zorder=z)
            z+=1
        if(plot_relative):
            england.plot(column=c_date.strftime('relative_%m%d'),ax=ax,cmap=colour_map,vmin=-2,vmax=2,zorder=z)
            z+=1
        if(plot_risk_weighted_ltla):
            england.plot(column=c_date.strftime('risk_%m%d'),ax=ax,cmap=colour_map,vmin=0.,vmax=ltla_vmax,zorder=z)
            z+=1
        if(plot_msoa_data):
            plot_msoa_outlines = False
            if plot_msoa_outlines: england.plot(column=c_date.strftime('msoa_%m%d'),ax=ax,facecolor="#DDBBBB",hatch="//",zorder=z,alpha=msoa_alpha)    
            else: england.plot(column=c_date.strftime('msoa_%m%d'),ax=ax,cmap=msoa_colour_map,vmin=3,vmax=30,zorder=z,alpha=msoa_alpha)
            z+=1
        if(plot_lsoa_data):
            lsoa_map.plot(column=c_date.strftime('lsoa_%m%d'),ax=ax,cmap=lsoa_colour_map,vmin=3,vmax=30,zorder=z,alpha=lsoa_alpha)
            z+=1
        if(plot_laa):
            england_laa.boundary.plot(ax=ax,zorder=z,linewidth=laa_linewidth,color='#553311')
            z+=1
        if(plot_electoral_boundaries):
            constituencies.boundary.plot(ax=ax,zorder=z,linewidth=laa_linewidth*5,color='#550000')
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
                        plt.text(laa_centroids[count][0],laa_centroids[count][1]+y_shift+yy_shift,name,horizontalalignment=al_mode,fontsize=laa_fontsize*0.6,bbox=dict(boxstyle='square',color='#AAAA8855'))
                    if plot_laa_values: plt.text(laa_centroids[count][0],laa_centroids[count][1]+y_shift-yy_shift,"%3.1f" % val,horizontalalignment=al_mode,fontsize=laa_fontsize) #bbox=dict(boxstyle='square',color='#FFFFEE11')
        if add_date: plt.text(label_x,label_y,c_date.strftime("%B %d"), horizontalalignment=text_align_mode, style='italic',fontsize=date_font_size)
        if add_title:plt.text(title_x,title_y,title_string,horizontalalignment=text_align_mode,fontsize=title_font_size)
        if add_footer:    
            footer = file_date.strftime(footer_message + " Data set published %d/%m/%y. github.com/jah-photoshop/autocovid")
            fr_scale = f_scale
            if(plot_laa_values): 
                footer = "Values are cases/100K/week. "+footer
                fr_scale = f_scale * 1.2
            plt.text(frame_margins[1]-( (frame_margins[1] - frame_margins[0]) * 0.01),frame_margins[2]+( (frame_margins[3] - frame_margins[2]) * 0.01),footer,horizontalalignment='right',fontsize=title_font_size / fr_scale, bbox=dict(boxstyle='square',color='#AAAA8844'))
        plt.savefig(f_string, bbox_inches='tight')
        if post_process:
            if resize_output: os.system('convert %s -resize %dx%d\! %s' % (f_string,target_width,target_height,f_string))
            if add_background: os.system('composite %s %s %s' % (f_string,background_file,f_string))
            if add_overlay: 
                for count, of in enumerate(overlay_filenames):
                    if of[-1]==os.path.sep: of+=c_date.strftime("map-%Y%m%d.png")
                    print(of)
                    if overlay_positions[count] == [0,0]: os.system('composite %s %s %s' % (of, f_string,f_string))                    
                    else: os.system('composite %s -geometry +%d+%d %s %s' % (of, overlay_positions[count][0],overlay_positions[count][1],f_string,f_string))
        fig.clf()   
        #Copy file to googledrive
        if(archive):
            if not os.path.exists(archive_path + short_name): os.makedirs(archive_path+short_name)
            shutil.copyfile(f_string,archive_path + short_name + os.path.sep + c_date.strftime("map-%Y%m%d.png"))
    print("________________________________________________________________________________")
print("Operation complete.")
