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


#Populations:  [githubcom/russss/covidtracker]
#London 8908081
#South East 8852361
#South West 5605997
#East of England 6493188
#Midlands 10537679
#North East and Yorkshire 8566925
#North West 7012947

reg_pops = [8.908081,8.852361,5.605997,6.493188,10.537679,8.566925,7.012947]
def_days = 0  #Plot since 20th March

debug = False
overwrite_mode = True           #If set to false, program will halt if output folder exists

data_path = "data"
output_path = "nhs"

archive_path = datetime.now().strftime("/home/robotlab/jah-photoshop-googledrive/output-%Y%m%d/")

#ltla_vmax=200

if(os.path.isdir(output_path)):
    if not overwrite_mode:
        print("Output path %s already exists; aborting" % (output_path))
        sys.exit()
        
nhs_map_filename = "zip://" + data_path + os.path.sep + "NHS_England_Regions__April_2020__Boundaries_EN_BUC-shp.zip"

admissions_filename = data_path + os.path.sep + "r_admissions.csv"

print("________________________________________________________________________________")
print("LOADING MAP DATA")
#Load map data for England [and Wales] from shape file
print("Loading NHS region map data from " + nhs_map_filename)
nhs=gpd.read_file(nhs_map_filename)
nhs_regions = nhs.nhser20nm.to_list()
print("________________________________________________________________________________")
print("LOADING ADMISSON DATA")
print("Loading admission data from " + admissions_filename)
with open(admissions_filename) as csv_file: ad_data = [row for row in csv.reader(csv_file, delimiter=',')][1:]
start_date = datetime(2021,12,30)
end_date = datetime(2020,1,1)
#regions = []
for data_line in ad_data:
    if data_line[0] not in nhs_regions: 
        print("Error: region mismatch")
        #regions.append(data_line[0])
    l_date = datetime.strptime(data_line[1],"%Y-%m-%d")
    if l_date > end_date: end_date=l_date
    if l_date < start_date: start_date = l_date
print(start_date.strftime('Start date: %d %m %Y'))
print(end_date.strftime('End date: %d %m %Y'))
number_of_days = (end_date-start_date).days + 1
number_of_regions = len(nhs_regions)
print("Number of days: %d" % number_of_days)
print("Number of regions: %d" % number_of_regions)
#admissions = [[0] * number_of_regions] * number_of_days
admissions = np.zeros((number_of_days,number_of_regions))
for data_line in ad_data:
    ix = nhs_regions.index(data_line[0])
    day_ix = (datetime.strptime(data_line[1],"%Y-%m-%d") - start_date).days
    val = int(data_line[2])
    admissions[day_ix][ix]=val

av_admissions = np.zeros((number_of_days,number_of_regions))
for day in range(number_of_days):
    start_day = day-6
    if day<6: start_day = 0
    n_days = day - start_day + 1
    for r in range(number_of_regions):
        sumt = 0
        for n in range(n_days):
            sumt += admissions[start_day + n][r]
        sumt /= n_days
        av_admissions[day][r] = sumt

ad_rate = np.zeros((number_of_days,number_of_regions))
for day in range(number_of_days):
    for r in range(number_of_regions):
        ad_rate[day][r]=admissions[day][r]/reg_pops[r]
max_admissions = np.max(admissions)
max_ad_rate = np.max(ad_rate)
max_ad_rate = 400
               
print("Building map data")
for day in range(number_of_days):
    c_date = start_date + timedelta(days=day)
    admissions_series = pd.Series(admissions[day])
    admissions_title = c_date.strftime('admissions_%m%d')
    nhs[admissions_title]=admissions_series
    ad_rate_series = pd.Series(ad_rate[day])
    ad_rate_title = c_date.strftime('rate_%m%d')
    nhs[ad_rate_title]=ad_rate_series

#            
print("________________________________________________________________________________")
print("PRODUCING PLOTS")

fig=plt.figure(figsize=(24.77,24.77),frameon=False)
if not os.path.exists(output_path): os.makedirs(output_path)
    
    
for day in range(def_days,number_of_days):
        c_date = start_date + timedelta(days=day)
        f_string = output_path+os.path.sep+c_date.strftime("map-%Y%m%d.png")
        print("Creating file %s" % (f_string))
        ax=plt.gca()
        ax.set_aspect('equal')
        ax.axis([132000, 659000, 9600, 675000])
        
        plt.axis('off')
        
        #nhs.plot(column=c_date.strftime('admissions_%m%d'),ax=ax,cmap='jet',vmin=0,vmax=max_admissions,zorder=0)
        nhs.plot(column=c_date.strftime('rate_%m%d'),ax=ax,cmap='jet',vmin=0,vmax=max_ad_rate,zorder=0)
        nhs.boundary.plot(ax=ax,zorder=1,linewidth=2,color='#22222288')

        plt.text(546000,590000,c_date.strftime("%B %d"), horizontalalignment='center', style='italic',fontsize=50)
        #plt.text(541000,655000,"Hospital Cases by Region",horizontalalignment='center',fontsize=42)
        plt.savefig(f_string, bbox_inches='tight')
       
        fig.clf() 
print("________________________________________________________________________________")
print("Operation complete.")
