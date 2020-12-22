#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
local_deaths.py

                                        
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
#  pip install matplotlib csv
  
import csv, math, os, sys
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

debug = True 

print("Local Death Data Plotter   -   Version 1.0   -   @jah-photoshop Dec 2020")
print("")
print("This script reads from the deaths and case data CSV           ")
print("")


f=plt.figure(figsize=(36,5),dpi=72,frameon=False) 

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
    
#Create output paths

output_path         = input("Enter output path   [default: deathplots]      : ") or "2nd_wave_plots"
#if os.path.exists(output_path): fail("Output path already exists (%s)" % (output_path))
os.mkdir(output_path)

cases_filename   = input("Enter cases filename [default: cases.csv]: ") or "cases.csv"

if not os.path.isfile(cases_filename): fail("Cases file not found (%s)" % (cases_filename))

deaths_filename = input("Enter deaths filename [default: deaths.csv]: ") or "deaths.csv"

if not os.path.isfile(cases_filename): fail("Deaths file not found (%s)" % (deaths_filename))

start_date_str   =      input("Start date for output [default: 2020-09-01]    : ") or "2020-09-01"
start_date = datetime.strptime(start_date_str,"%Y-%m-%d")

case_data = read_file(cases_filename)

dates = []
#start_date = datetime(2020,8,1)

end_date = start_date
area_codes = []
area_names = []



for count,line in enumerate(case_data):
    if count > 0:
        try:
            e_date = datetime.strptime(line[3],"%Y-%m-%d")
            if line[1] not in area_codes: 
                area_codes.append(line[1])
                area_names.append(line[0])
            if (e_date > end_date): end_date = e_date
            dates.append(e_date)
        except:
            print("Error on line %d:%s" % (count,line))

area_pop = [0] * len(area_codes)

surpress_days = 1
last_date = end_date - timedelta(days=surpress_days)
d_start_date = datetime.strptime("2020-03-01","%Y-%m-%d")

no_days = (last_date - d_start_date).days

area_cases = []
area_7day_av = []
area_case_rate = []

for i in range(len(area_codes)): 
    area_cases.append([0] * no_days)
    area_7day_av.append([0.0] * no_days)
    area_case_rate.append([0.0] * no_days)


for count,line in enumerate(case_data[1:]):
      e_date = datetime.strptime(line[3],"%Y-%m-%d")
      if e_date==end_date:
          area_pop[area_codes.index(line[1])] = (100000.0 * float(line[5])) / float(line[6])
      offset = (e_date - d_start_date).days
      if offset>=0 and offset<no_days:
          area_cases[area_codes.index(line[1])][offset] = int(line[4])
        
for count,cases in enumerate(area_cases):
    for ind,el in enumerate(cases):
        sp = ind - 6
        la = 7
        if sp < 0:
            la += sp
            sp = 0
        a_sum = sum(cases[sp:(ind + 1)])
        area_7day_av[count][ind]=float(a_sum)/la
        area_case_rate[count][ind]=area_7day_av[count][ind] * 700000 / area_pop[count] #Cases/100k/week

    
    
    
print ("Case data range covers %d days (from %s until %s)" % (no_days,start_date.strftime("%Y-%m-%d"),last_date.strftime("%Y-%m-%d")))

    
deaths_data = read_file(deaths_filename)[1:]

area_total_deaths = []
area_covid_deaths = []
area_total_deathcount = []
area_covid_deathcount = []
area_total_deathrate = []
area_covid_deathrate = []
area_covid_deathpercentage = []

first_week = 1
last_week = 1
death_locations = []
for count,line in enumerate(deaths_data):
    if line[5] not in death_locations:
        death_locations.append(line[5])
    if int(line[4]) > last_week: last_week = int(line[4])    

week_dates = []
qwd = datetime.strptime("2020-01-03","%Y-%m-%d")
for p in range(last_week):
    week_dates.append(qwd + timedelta(days=(7 * p)))
    
day_dates = []
for p in range(no_days):
    day_dates.append(d_start_date + timedelta(days=p))
    
for i in range(len(area_codes)): 
    p_w = []
    for p in range(last_week):
        w_d = [0] * len(death_locations)
        p_w.append(w_d)
    area_total_deaths.append(p_w)

for i in range(len(area_codes)): 
    p_w = []
    for p in range(last_week):
        w_d = [0] * len(death_locations)
        p_w.append(w_d)
    area_covid_deaths.append(p_w)
    
for count,line in enumerate(deaths_data):
    if line[0] in area_codes:
        ind = area_codes.index(line[0])
        loc = death_locations.index(line[5])
        week = int(line[4])
        d_count = int(line[6])
        if line[3]=='All causes':
            area_total_deaths[ind][week - 1][loc] = d_count
        else:
            area_covid_deaths[ind][week - 1][loc] = d_count
            
        
for i in range(len(area_codes)):
    area_total_deathcount.append([])
    area_covid_deathcount.append([])
    area_total_deathrate.append([])
    area_covid_deathrate.append([])
    area_covid_deathpercentage.append([])
    for w in range(last_week):
        area_total_deathcount[i].append(sum(area_total_deaths[i][w]))
        area_covid_deathcount[i].append(sum(area_covid_deaths[i][w]))
        if area_total_deathcount[i][w] == 0: area_covid_deathpercentage[i].append(0.0)
        else: area_covid_deathpercentage[i].append(float(100.0 * area_covid_deathcount[i][w]) / area_total_deathcount[i][w])
        #    print("Area code not found in case data: %s" % line)
        
         
def plot_chart(index):
    f_string=output_path+os.path.sep + area_codes[index]+"_"+area_names[index]+".png"
    f=plt.figure(figsize=(16,6),dpi=72,frameon=True) 
    q_offset= (start_date - d_start_date).days
    d_max = max(area_total_deathcount[index])
    c_max = max(area_7day_av[index])
    b_max = c_max
    if d_max > b_max : b_max = d_max
    b_max *= 1.05
    plt.axis([start_date,end_date,0,b_max])
    #plt.bar(day_dates,area_cases[index])
    plt.bar(week_dates,area_total_deathcount[index],width=6,color="#DDDDDDCC",label='Total Deaths')
    plt.bar(week_dates,area_covid_deathcount[index],width=6,color="#FFAA22FF",label='Covid Deaths')
    plt.plot(day_dates[q_offset:],area_7day_av[index][q_offset:],label='Covid Cases')
    plt.title("COVID: Daily Cases and Weekly Deaths for %s" % area_names[index],fontsize='x-large')
    legend=plt.legend(loc='upper left',shadow=True,fontsize='large')
    legend.get_frame().set_facecolor('#FCFCE6EE')
    plt.text(end_date-timedelta(days=1),b_max*0.92,"Data source: coronavirus.data.gov.uk",horizontalalignment='right',fontsize='small')
    plt.text(end_date-timedelta(days=1),b_max*0.893,"and ons.gov.uk, capture 22/12/2020",horizontalalignment='right',fontsize='small')
    #plt.show()
    plt.savefig(f_string, bbox_inches='tight')

for i in range(len(area_codes)):
    plot_chart(i)
    