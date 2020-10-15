#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autocovid.py


This script generates a series of .PNG files (which can be converted into a 
video using FFMPEG etc) from the combined data file.

                                              
MIT License

Copyright 2020 - @jah-photoshop

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

@author: @jah-photoshop

"""

#  Tested on Ubuntu (20.04) with Python 3.8.2
#  Prerequisits:  
#  sudo apt install imagemagick ffmpeg
#  pip install matplotlib csv geopandas
  
import csv, math, os, sys
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

print("Autocovid - Version 1.1 - @jah-photoshop Oct 2020")
print("")
print("This script reads from the combined data csv and plots as series of PNG")
print("")

#Some parameters that may want to be tweaked...
debug = False            # Set to True to print extended debug information whilst processing
plot_region_stats = False # Set to True to include regional statistics legend on map
merge_plots = True

surpress_days = timedelta(days=3)
plt.rcParams.update({'font.size': 26})
plt.rcParams.update({'axes.linewidth': 0})

f=plt.figure(figsize=(36,5),dpi=72,frameon=False) 
a_bar_col = "#2266AA"
a_line_col = "#EE3333"
a_edge_col = "#5599CC"
i_bar_col = "#CCCCE0"
i_line_col = "#FFBBBB"
i_edge_col = "#BBBBDD"


#Parse a CSV file and read data lines into list
def read_file(filename):
    data = []
    if(debug): print ("Opening file %s" % (filename))
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
          data.append(row)
    if(debug): print(f'Processed {len(data)} lines.')
    return (data)

#There has been a problem...
def fail(message):
    print("There has been an error:")
    print(message)
    sys.exit()
    
def annotate_picture(filename,list_of_annotations):
    annotate_string = "convert %s -gravity SouthEast -pointsize 23 " % filename
    for annotation in list_of_annotations:
        cs = "'#EEEE'"
        if(annotation[5]): cs = "'#DDDD'"
        if(annotation[6]): cs = "'#888C'"
        if(annotation[3]):  #Right justified for numerical entries
            sub_string =  " -gravity SouthEast -font FreeMono-Bold -pointsize %d -stroke '#222C' -strokewidth 1 -annotate +%d+%d '%s' " % (annotation[4],annotation[0],annotation[1],annotation[2])
            sub_string += "-stroke none -fill %s -annotate +%d+%d '%s' " % (cs,annotation[0],annotation[1],annotation[2])
        else:
            sub_string =  " -gravity SouthWest -font Lato-Bold -pointsize %d -stroke '#000C' -strokewidth 2 -annotate +%d+%d '%s' " % (annotation[4],annotation[0],annotation[1],annotation[2])
            sub_string += "-stroke none -fill %s -annotate +%d+%d '%s' " % (cs,annotation[0],annotation[1],annotation[2])           
        annotate_string += sub_string
    annotate_string += filename
    #print(annotate_string)
    os.system(annotate_string)
        
def get_ra(list_in):
    ra = []
    for count,entry in enumerate(list_in):
        cra = 0
        for k in range(7):
            if count + k < len(list_in): cra += list_in[count+k]
        dra = cra / 7.0
        ra.append(dra)
    return ra

#Create output paths
output_path         = input("Enter output path   [default: plots]           : ") or "plots"
bg_output_path = output_path + os.path.sep + 'backgrounds'
if os.path.exists(bg_output_path): fail("Output path already exists (%s)" % (bg_output_path))
#os.mkdir(output_path)


cases_filename   = input("Enter data filename [default: data/england.csv]: ") or "data/england.csv"

if not os.path.isfile(cases_filename): fail("Combined data file not found (%s)" % (cases_filename))

heatmap_folder = input("Enter map filepath  [default: autocovid_map]: ") or "autocovid_map"

if not os.path.exists(output_path + os.path.sep + heatmap_folder): fail("Heatmap image path not found (%s)" % (heatmap_folder))


os.mkdir(output_path + os.path.sep + 'temp')
merged_output_path = output_path + os.path.sep + 'merged'

os.mkdir(bg_output_path)
os.mkdir(merged_output_path)

#Background image is merged with each output frame using convert (imagemagick)
background_filename   = input("Background image filename [default: bg.png]    : ") or "bg.png"
if not os.path.isfile(background_filename): fail("Background image file not found (%s)" % (background_filename))

annotate_events_r     = input("Annotate timeline events [default: yes]        : ") or "yes"
annotate_events = False
if annotate_events_r.startswith('y'): annotate_events = True

event_dates = []
event_strings = []

if(annotate_events):
    annotate_filename =     input("Annotations .CSV filename [default: events.csv]: ") or "events.csv"
    if not os.path.isfile(annotate_filename): fail("Events file not found (%s)" % (annotate_filename))
    events_data = read_file(annotate_filename)
    for count, line in enumerate(events_data):
        try:
            e_date = datetime.strptime(line[0],"%Y-%m-%d")
            event_dates.append(e_date)
            event_strings.append(line[1])
        except:
            print("Error on line %d:%s" % (count,line))
            

shade_regions_r     = input("Shade regions by case rate [default: no]      : ") or "no"
shade_regions = False
if shade_regions_r.startswith('y'): shade_regions = True


regions = ['northwest','northeast','yorkshire','westmidlands','eastmidlands','east','southwest','southeast','london']
#regions_format = ['North West','North East','Yorkshire and Humberi','West Midlands','East Midlands','East of England','South West','South East','London']
region_rates = []
region_dates = []
if(shade_regions):
    for count, region in enumerate(regions):
        region_date = []
        reg_fn = "data" + os.path.sep + region + '.csv'
        region_data = read_file(reg_fn)[1:]
        region_cases = [int(el[1]) for el in region_data]
        region_dates.append([datetime.strptime(el[0], "%Y-%m-%d") for el in region_data] )
        region_cases_av = get_ra(region_cases)
        region_pop = int(region_data[0][2]) / float(region_data[0][3]) #Population [in 100Ks]
        region_rate = [(7.0 * el) / region_pop for el in region_cases_av]        
        region_rates.append(region_rate)
        print ("%s: Max: %f" % (region,max(region_rate)))
    
start_date_str   =      input("Start date for output [default: 2020-03-04]    : ") or "2020-03-04"
start_date = datetime.strptime(start_date_str,"%Y-%m-%d")
if not os.path.isfile(background_filename): fail("Background image file not found (%s)" % (background_filename))



data = read_file(cases_filename)

dates = []
#start_date = datetime(2020,8,1)

end_date = start_date


for count,line in enumerate(data):
    if count > 0:
        try:
            e_date = datetime.strptime(line[0],"%Y-%m-%d")
            if (e_date > end_date): end_date = e_date
            dates.append(e_date)
        except:
            print("Error on line %d:%s" % (count,line))
            
            
            
#print(dates)
#print(cases)
no_days = (end_date - start_date - surpress_days).days
charts_to_plot = ['Cases','Admissions','Patients','Ventilated','Deaths']
headers = data[0]
plot_list = []
for chart in charts_to_plot:
    plot_list.append(headers.index(chart))


for day in range(no_days):
#for day in range(1):
    annotation_list = []
    day_d = timedelta(days=(day))
    c_day = start_date + day_d - timedelta(days=1)
    print ("Generating plots for %s" % (c_day.strftime("%Y-%m-%d")))
    ofn_list = []
    for c_c, column_ix in enumerate(plot_list):
        chart = data[0][column_ix]
        pre_cases = []
        post_cases = []
        pre_dates = []
        post_dates = []
        pre_avs = []
        post_avs = []
        cases = []
        c_max = 0
        for line in (data[1:]):
            if(line[column_ix] == ''): 
                    cases.append(0)
            else:
                    e_cases = int(line[column_ix])
                    cases.append(e_cases)
        avs = get_ra(cases)
        for count,entry in enumerate(dates):
            if entry>=start_date and cases[count]>c_max: c_max = cases[count]

            if start_date + day_d > entry:
                pre_cases.append(cases[count])
                pre_dates.append(entry)
                pre_avs.append(avs[count])
            else:
                post_cases.append(cases[count])
                post_dates.append(entry)
                post_avs.append(avs[count])
                
        plt.axis([start_date-timedelta(hours=36),end_date-surpress_days-timedelta(hours=30),0,c_max*1.02])
        ax=plt.gca()
        pad_w= -10 - ( len("%d" % c_max) * 14)
        ax.tick_params(axis="y", direction="in", pad=pad_w)
        ax.tick_params(axis="x", direction="in")
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_visible(False)
        yticks = ax.yaxis.get_major_ticks()
        yticks[0].label1.set_visible(False)
        plt.bar(pre_dates,pre_cases,width=0.6,color=a_bar_col,edgecolor=a_edge_col,linewidth=0.72)
        plt.plot(pre_dates,pre_avs,color=a_line_col,linewidth=6)
        plt.bar(post_dates,post_cases,width=0.6,color=i_bar_col,edgecolor=i_edge_col,linewidth=0.72)
        plt.plot(post_dates,post_avs,color=i_line_col,linewidth=6)
        plt.axvline(x=c_day+timedelta(hours=8), color="#552255", ls=':', lw=3)
        annotation_list.append([1120,882 - (c_c * 174),"%d" % int(pre_cases[0]),True,24,False,False])
        annotation_list.append([890,882 - (c_c * 174),"%d" % int(pre_avs[0]),True,24,False,False])        
        ofn = output_path + os.path.sep + "temp" + os.path.sep + chart + ".png"
        ofn_list.append(ofn)
        plt.savefig(ofn, bbox_inches='tight',transparent=True)
        f.clf()
        #Call convert (from imagemagick package) to resize image to 900x124 pixels
        os.system('convert %s -trim -resize 1000x124\! %s' % (ofn,ofn))        
    frame_name = bg_output_path + os.path.sep + c_day.strftime("%Y%m%d.png")
    #Call convert to merge all frames
    print("Compositing images")
    os.system('cp %s %s' % (background_filename,frame_name))
    for count,figfn in enumerate(ofn_list):
        os.system('composite -geometry +30+%d %s %s %s' % (200 + (count * 174),figfn,frame_name,frame_name))
    print("Annotating images")
    #x_day = c_day - timedelta(days=1)
    annotation_list.append([34,940,c_day.strftime("%a %d %b"),False,48,False,False])
    if(annotate_events):
        draw_event = False
        date_string = ""
        e_string = ""
        fade = False
        for count,edate in enumerate(event_dates):
            date_delta = c_day - edate
            if(date_delta.days >= 0 and date_delta.days < 3):
                if(date_delta.days > 0):
                    fade = True
                draw_event = True
                date_string = edate.strftime("%d %b")
                e_string = event_strings[count]
        if(draw_event):
            annotation_list.append([360,976,date_string,False,18,fade,False])
            annotation_list.append([360,940,e_string,False,32,fade,False])
        
    annotate_picture(frame_name,annotation_list)
    if(shade_regions):
        print("Shading regional data")
        region_annotations = []
        if(plot_region_stats):
            os.system('composite -geometry +1668+30 regions/backlayer.png %s %s' % (frame_name,frame_name))

        for count,region in enumerate(regions): 
            rate = 0
            if c_day in region_dates[count]:
                date_index = region_dates[count].index(c_day)
                rate = region_rates[count][date_index]
                if rate is None: rate = 0
                region_annotations.append([38,982 - (count * 24),"%3.1f" % rate,True,20,False,True])
            if(rate > 100):rate=100
            if(rate < 0): rate = 0
            reg_sep = ""
            if (plot_region_stats): reg_sep = "-e"
            region_filename="regions" + os.path.sep + region + reg_sep + ".png"
            os.system('composite -dissolve %f -geometry +985+26 %s %s %s' % (rate,region_filename,frame_name,frame_name))
        if(plot_region_stats):
            os.system('composite -geometry +1668+30 regions/overlay.png %s %s' % (frame_name,frame_name))
            print("Annotating regional data")
            annotate_picture(frame_name,region_annotations)
    if merge_plots:
        heatmap_file = output_path + os.path.sep + heatmap_folder + os.path.sep + c_day.strftime("map-%Y%m%d.png")
        merged_file = merged_output_path + os.path.sep + c_day.strftime("merged-%Y%m%d.png")
        os.system('composite -geometry +1045+10 %s %s %s' % (heatmap_file,frame_name,merged_file))
        
        #Add London overlay and key
        london_overlay_folder = 'autocovid_london'
        london_file = output_path + os.path.sep + london_overlay_folder + os.path.sep + c_day.strftime("map-%Y%m%d.png")
        os.system('composite -geometry +1627+17 %s %s %s' % (london_file,merged_file,merged_file))
        
        legend_file = 'autocovid_key.png'
        os.system('composite -geometry +1096+456 %s %s %s' % (legend_file,merged_file,merged_file))
