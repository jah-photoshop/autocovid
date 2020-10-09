#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_presets.py

Generate preset (.pickle) files 

Created on Wed Oct  7 13:55:28 2020

"""
import os, pickle
preset_folder = "presets"
background_file = ""

if(not os.path.isdir(preset_folder)): os.makedirs(preset_folder)


def write_pickle():
    d_list=[short_name,plot_msoa_boundaries,target_places,colour_map,msoa_colour_map,lsoa_colour_map,msoa_alpha,lsoa_alpha,frame_margins,label_x,label_y,title_x,title_y,plot_wales,plot_scotland,plot_towns,
            plot_laa,title_string,laa_linewidth,standalone_plot,post_process,resize_output,
            heat_lim,transparent,add_date,add_background,add_overlay,add_title,target_width,
            target_height,plot_laa_names,plot_laa_values,plot_ltla_data,plot_msoa_data,plot_lsoa_data,plot_combined_data,text_align_mode,
            date_font_size,title_font_size,laa_fontsize,mask_colour,add_footer,restrict_laa_to_targets,f_scale,overlay_filename,background_file]
    with open(preset_folder+os.path.sep+short_name+".pickle","wb") as f: pickle.dump(d_list,f)        




#Default (England, combined data, with background)
short_name="default"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=0.4
frame_margins = [133000,658000,10600,655000]
label_x=650000
label_y=576000
title_x=650000
title_y=605000
plot_msoa_boundaries=True
plot_wales=True
plot_scotland=True
plot_towns=False
plot_laa = True
title_string = "Covid-19 Heatmap"
laa_linewidth= 0.6
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 10
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1080
target_height = 1324
plot_laa_names=False
plot_laa_values=False
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'right'
date_font_size = 80
title_font_size = 70
laa_fontsize = 14
mask_colour='#EEEEEE'
add_footer = True
restrict_laa_to_targets = False
f_scale = 3.3
overlay_filename = ''
write_pickle()

#LTLA Heatmap
short_name="ltla"
target_places = []
colour_map='YlGnBu'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=0.4
frame_margins = [132000,659000,9600,675000]
label_x=545000
label_y=596000
title_x=650000
title_y=605000
plot_msoa_boundaries=False
plot_wales=True
plot_scotland=True
plot_towns=False
plot_laa = True
title_string = "Covid-19 LTLA Heatmap"
laa_linewidth= 0.6
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 10
transparent = True
add_date = True
add_background = True
add_overlay = True
add_title = False
target_width  = 1080
target_height = 1360
plot_laa_names=False
plot_laa_values=False
plot_ltla_data = True
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = False
text_align_mode = 'center'
date_font_size = 76
title_font_size = 54
laa_fontsize = 14
mask_colour='#406080'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.72
overlay_filename = 'ltla-fg.png'
background_file = "ltla-bg.png"
write_pickle()


#Heatmap with background image
short_name="heatmap"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=0.4
frame_margins = [133000,658000,10600,655000]
label_x=547000
label_y=576000
title_x=650000
title_y=605000
plot_msoa_boundaries=True
plot_wales=True
plot_scotland=True
plot_towns=False
plot_laa = True
title_string = "Covid-19 Heatmap"
laa_linewidth= 0.6
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 10
transparent = True
add_date = True
add_background = True
add_overlay = False
add_title = False
target_width  = 1080
target_height = 1324
plot_laa_names=False
plot_laa_values=False
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'center'
date_font_size = 64
title_font_size = 70
laa_fontsize = 14
mask_colour='#122B49'
add_footer = False
restrict_laa_to_targets = False
f_scale = 3.3
overlay_filename = ''
background_file = "heatmap.png"
write_pickle()



#MSOA Only Plot 
short_name="msoa"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='winter'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=0.4
frame_margins = [133000,658000,10600,655000]
label_x=654000
label_y=576000
title_x=654000
title_y=605000
plot_msoa_boundaries=True
plot_wales=True
plot_scotland=True
plot_towns=False
plot_laa = True
title_string = "MSOA Covid Outbreaks in England"
laa_linewidth= 0.6
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 10
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1080
target_height = 1324
plot_laa_names=False
plot_laa_values=False
plot_ltla_data = False
plot_msoa_data = True
plot_lsoa_data = False
plot_combined_data =  False
text_align_mode = 'right'
date_font_size = 70
title_font_size = 38
laa_fontsize = 14
mask_colour='#EEEEEE'
add_footer = True
restrict_laa_to_targets = False
f_scale = 1.8
overlay_filename = ''
background_file=''
write_pickle()

#LSOA Only Plot 
short_name="lsoa"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='summer'
msoa_alpha=1
lsoa_alpha=1
frame_margins = [133000,658000,10600,655000]
label_x=654000
label_y=576000
title_x=654000
title_y=605000
plot_msoa_boundaries=True
plot_wales=True
plot_scotland=True
plot_towns=False
plot_laa = True
title_string = "LSOA Covid Outbreaks in England"
laa_linewidth= 0.5
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 10
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1080
target_height = 1324
plot_laa_names=False
plot_laa_values=False
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = True
plot_combined_data =  False
text_align_mode = 'right'
date_font_size = 70
title_font_size = 38
laa_fontsize = 14
mask_colour='#EEEEEE'
add_footer = True
restrict_laa_to_targets = False
f_scale = 1.8
overlay_filename = ''
background_file=''
write_pickle()

#LSOA data on top of MSOA\LTLA combi Plot 
short_name="combined"
target_places = []
colour_map='Oranges'
msoa_colour_map='YlOrRd'
lsoa_colour_map='Autumn'
msoa_alpha=1
lsoa_alpha=0.4
frame_margins = [133000,658000,10600,655000]
label_x=654000
label_y=576000
title_x=654000
title_y=605000
plot_msoa_boundaries=True
plot_wales=True
plot_scotland=True
plot_towns=False
plot_laa = True
title_string = "Local Covid Outbreaks in England"
laa_linewidth= 0.5
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 10
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1080
target_height = 1324
plot_laa_names=False
plot_laa_values=False
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = True
plot_combined_data =  True
text_align_mode = 'right'
date_font_size = 66
title_font_size = 38
laa_fontsize = 14
mask_colour='#EEEEEE'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2
overlay_filename = ''
background_file=''
write_pickle()

#East England
short_name="east"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=1
frame_margins = [500000,659000,160000,360000]
label_x=655000
label_y=193000
title_x=655000
title_y=350000
plot_msoa_boundaries=True
plot_wales=False
plot_scotland=False
plot_towns=True
plot_laa = True
title_string = "Heatmap for East of England"
laa_linewidth= 2
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 8
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1080
target_height = 1353
plot_laa_names=False
plot_laa_values=True
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'right'
date_font_size = 80
title_font_size = 60
laa_fontsize = 18
mask_colour='#122B49'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.67
overlay_filename=''
background_file=''
write_pickle()


#South East England
short_name="southeast"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=1
frame_margins = [400000,640000,80000,240000]
label_x=637000
label_y=89000
title_x=630000
title_y=232000
plot_msoa_boundaries=True
plot_wales=False
plot_scotland=False
plot_towns=True
plot_laa = True
title_string = "Heatmap for South East England"
laa_linewidth= 2
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 8
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1615
target_height = 1080
plot_laa_names=False
plot_laa_values=True
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'right'
date_font_size = 80
title_font_size = 60
laa_fontsize = 14
mask_colour='#122B49'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.5
overlay_filename=''
background_file=''
write_pickle()

#Midlands
short_name="midlands"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=1
frame_margins = [315000,560000,210000,412000]
label_x=317000
label_y=392000
title_x=317000
title_y=402000
plot_msoa_boundaries=True
plot_wales=True
plot_scotland=False
plot_towns=True
plot_laa = True
title_string = "Heatmap for Midlands"
laa_linewidth= 2
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 8
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1308
target_height = 1080
plot_laa_names=True
plot_laa_values=True
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'left'
date_font_size = 80
title_font_size = 60
laa_fontsize = 20
mask_colour='#DDDDDD'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.4
overlay_filename=''
background_file=''
write_pickle()


#Yorkshire+Humber Region
short_name="yorkshire"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=1
frame_margins = [360000,560000,390000,525000]
label_x=556000
label_y=505000
title_x=556000
title_y=515000
plot_msoa_boundaries=True
plot_wales=True
plot_scotland=False
plot_towns=True
plot_laa = True
title_string = "Heatmap for Yorkshire and Humber"
laa_linewidth= 2
standalone_plot = True
post_process = True
resize_output = False
heat_lim = 8
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1308
target_height = 1080
plot_laa_names=False
plot_laa_values=True
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'right'
date_font_size = 80
title_font_size = 40
laa_fontsize = 20
mask_colour='#DDDDDD'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.4
overlay_filename=''
background_file=''
write_pickle()


#South West England
short_name="southwest"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=1
frame_margins = [133000,465000,10600,254000]
label_x=143000
label_y=165000
title_x=298000
title_y=42000
plot_msoa_boundaries=True
plot_wales=True
plot_scotland=False
plot_towns=True
plot_laa = True
title_string = "Heatmap for South West England"
laa_linewidth= 1.2
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 6
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1474
target_height = 1080
plot_laa_names=False
plot_laa_values=True
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'left'
date_font_size = 80
title_font_size = 60
laa_fontsize = 14
mask_colour='#122B49'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.5
overlay_filename=''
background_file=''
write_pickle()

#North East England
short_name="northeast"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=1
frame_margins = [354000,480000,500000,660000]
label_x=477000
label_y=640000
title_x=477000
title_y=650000
plot_msoa_boundaries=True
plot_wales=False
plot_scotland=True
plot_towns=True
plot_laa = True
title_string = "Heatmap for North East England"
laa_linewidth= 2
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 10
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1080
target_height = 1369
plot_laa_names=True
plot_laa_values=True
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'right'
date_font_size = 80
title_font_size = 50
laa_fontsize = 22
mask_colour='#DDDDDD'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.3
overlay_filename=''
background_file=''
write_pickle()

#North West England
short_name="northwest"
target_places = []
colour_map='YlOrRd'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=1
frame_margins = [285000,415000,350000,585000]
label_x=288000
label_y=565000
title_x=288000
title_y=575000
plot_msoa_boundaries=True
plot_wales=True
plot_scotland=True
plot_towns=True
plot_laa = True
title_string = "Heatmap for North West England"
laa_linewidth= 2
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 10
transparent = False
add_date = True
add_background = False
add_overlay = False
add_title = True
target_width  = 1068
target_height = 1920
plot_laa_names=True
plot_laa_values=True
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'left'
date_font_size = 60
title_font_size = 40
laa_fontsize = 20
mask_colour='#DDDDDD'
add_footer = True
restrict_laa_to_targets = False
f_scale = 3.1
overlay_filename=''
background_file=''
write_pickle()






#North Yorkshire
short_name="northyorkshire"
frame_margins = [360000,520000,412000,520000]
target_places = ['Craven','Harrogate','Richmondshire','Hambleton','Ryedale','Scarborough','York','Selby']
colour_map='Greens'
msoa_colour_map='YlOrRd'
lsoa_colour_map='YlOrRd'
msoa_alpha=1
lsoa_alpha=1
label_x=518000
label_y=514500
title_x=300000
title_y=50000
plot_msoa_boundaries=True
plot_wales=False
plot_scotland=False
plot_towns=True
plot_laa = True
title_string = ""
laa_linewidth= 2
resize_output = True
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 8
transparent = False
add_date = True
add_background = False
add_overlay = True
add_title = False
target_width = 1594
target_height = 1080
plot_laa_names=True
plot_laa_values=True
plot_ltla_data = False
plot_msoa_data = False
plot_lsoa_data = False
plot_combined_data = True
text_align_mode = 'right'
date_font_size = 60
title_font_size = 60
laa_fontsize=40
mask_colour='#122B49'
add_footer = False
restrict_laa_to_targets = True
f_scale = 2.5
overlay_filename='graphics/overlay-nyorks.png'
background_file=''
write_pickle()


#North Yorkshire
short_name="nyorks-lsoa"
frame_margins = [360000,520000,412000,520000]
target_places = ['Craven','Harrogate','Richmondshire','Hambleton','Ryedale','Scarborough','York','Selby']
colour_map='BuGn'
msoa_colour_map='Summer'
lsoa_colour_map='Wistia'
colour_map='Oranges'
msoa_colour_map='Reds'
lsoa_colour_map='autumn'
msoa_alpha=0.2
lsoa_alpha=0.15
label_x=518000
label_y=514500
title_x=300000
title_y=50000
plot_msoa_boundaries=True
plot_wales=False
plot_scotland=False
plot_towns=True
plot_laa = True
title_string = ""
laa_linewidth= 2
resize_output = True
standalone_plot = True
post_process = True
resize_output = True
heat_lim = 8
transparent = False
add_date = True
add_background = False
add_overlay = True
add_title = False
target_width = 1594
target_height = 1080
plot_laa_names=True
plot_laa_values=True
plot_ltla_data = True
plot_msoa_data = True
plot_lsoa_data = True
plot_combined_data = False
text_align_mode = 'right'
date_font_size = 60
title_font_size = 60
laa_fontsize=40
mask_colour='#122B49'
add_footer = False
restrict_laa_to_targets = True
f_scale = 2.5
overlay_filename='graphics/overlay-nyorks.png'
background_file=''
write_pickle()
