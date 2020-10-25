#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 19:53:16 2020

@author: robotlab
"""

import csv, math, os, sys
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

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


brackets = [45,65,75,85]

datafile = "ltla-ages.csv"
data = read_file(datafile)
print("Read %d lines" % len(data))
print ("{AREA} : [0-44, 45-64, 65-74, 75-84, 85+]")
names = []
values = []
ids = []
for entry in data:
    n_id = entry[0]
    n_name = entry[1]
    age_vals = []
    n_total = int(entry[3].replace(',',''))
    for i in range(91):
        age_vals.append(int(entry[i+4].replace(',','')))
    if(sum(age_vals) != n_total): print("Error: Totals to not match total")
    sub_list = []
    bs = 0
    for b in brackets:
        sub_list.append(sum(age_vals[bs:b]))
        bs = b
    sub_list.append(sum(age_vals[bs:]))
    pct_vals = [e/n_total for e in sub_list]
    print("%s: %s" % (n_name,pct_vals) )
   
    death_ratios = [0.019867459,0.373875,1.479982,5.347738,16.91637]
    #tot = 53187
    
    adj_v = [death_ratios[c] * i for c,i in enumerate(pct_vals)]
    #print ("T:%d  C:%d" % (n_total,sum(sub_list) ) )
  #  print ("%s: %f" % (n_name,sum(adj_v) ))
    ids.append(n_id)
    names.append(n_name)
    values.append(sum(adj_v))
with open ('age_risk_index.csv','w') as f:
    for count,i in enumerate(ids):
        f.write("%s,%s,%f\n" % (i,names[count].replace(',',''),values[count]))



    