#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_presets.py

Generate preset (.pickle) files 

Created on Wed Oct  7 13:55:28 2020

"""
import os, pickle
preset_folder = "presets"
if(not os.path.isdir(preset_folder)): os.makedirs(preset_folder)


def write_pickle():
    d_list=[short_name,target_places,colour_map,frame_margins,label_x,label_y,title_x,title_y,plot_wales,plot_scotland,plot_towns,
            plot_laa,title_string,laa_linewidth,standalone_plot,post_process,resize_output,
            heat_lim,transparent,add_date,add_background,add_overlay,add_title,target_width,
            target_height,plot_laa_names,plot_laa_values,plot_combined_data,text_align_mode,
            date_font_size,title_font_size,laa_fontsize,mask_colour,add_footer,restrict_laa_to_targets,f_scale,overlay_filename]
    with open(preset_folder+os.path.sep+short_name+".pickle","wb") as f: pickle.dump(d_list,f)        




#Default (England, combined data, with background)
short_name="default"
target_places = []
colour_map='YlOrRd'
frame_margins = [133000,658000,10600,655000]
label_x=650000
label_y=576000
title_x=650000
title_y=605000
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

#East England
short_name="east"
target_places = []
colour_map='YlOrRd'
frame_margins = [500000,659000,160000,360000]
label_x=655000
label_y=193000
title_x=655000
title_y=350000
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
plot_combined_data = True
text_align_mode = 'right'
date_font_size = 80
title_font_size = 60
laa_fontsize = 14
mask_colour='#122B49'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.67
overlay_filename=''
write_pickle()


#South East England
short_name="southeast"
target_places = []
colour_map='YlOrRd'
frame_margins = [400000,640000,80000,240000]
label_x=580000
label_y=86000
title_x=404000
title_y=232000
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
target_width  = 1440
target_height = 1080
plot_laa_names=False
plot_laa_values=True
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
write_pickle()

#Midlands
short_name="midlands"
target_places = []
colour_map='YlOrRd'
frame_margins = [315000,560000,210000,412000]
label_x=317000
label_y=392000
title_x=317000
title_y=402000
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
plot_laa_names=False
plot_laa_values=True
plot_combined_data = True
text_align_mode = 'left'
date_font_size = 80
title_font_size = 60
laa_fontsize = 20
mask_colour='#DDDDDD'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.5
overlay_filename=''
write_pickle()


#Yorkshire+Humber Region
short_name="yorkshire"
target_places = []
colour_map='YlOrRd'
frame_margins = [360000,560000,390000,525000]
label_x=362000
label_y=492000
title_x=362000
title_y=502000
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
plot_combined_data = True
text_align_mode = 'left'
date_font_size = 80
title_font_size = 60
laa_fontsize = 20
mask_colour='#DDDDDD'
add_footer = True
restrict_laa_to_targets = False
f_scale = 2.5
overlay_filename=''
write_pickle()


#South West England
short_name="southwest"
target_places = []
colour_map='YlOrRd'
frame_margins = [133000,465000,10600,254000]
label_x=143000
label_y=165000
title_x=300000
title_y=50000
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
write_pickle()








#North Yorkshire
short_name="northyorkshire"
frame_margins = [360000,520000,412000,520000]
target_places = ['Craven','Harrogate','Richmondshire','Hambleton','Ryedale','Scarborough','York','Selby']
colour_map='Greens'
label_x=518000
label_y=514500
title_x=300000
title_y=50000
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
write_pickle()

