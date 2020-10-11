# autocovid
Scripts and tools to automate the plotting of England\UK Covid stats using data from coronavirus.data.gov.uk

The main program for generating map images is map_plot.py

download_data.sh downloads relevant .CSV files using cURL from coronavirus.data.gov.uk links [links obtained via Firefox 29/09/2020]
download_data_backup.sh is updated to work with map_plot (downloading cases, MSOA and LSOA files)

As of 11/10/2020 this looks like its broken - not sure if site has moved from azure or cookies issue.  
The files can all be manually downloaded from coronavirus.data.gov.uk and added to data folder as needed

In addition to cases data, a number of shape .zip files (mapping data) from the ONS Open Geography Portal are required.

The mapping files are available in a number of different resolution levels - the finest levels are very large files and
have a significant impact on run-time for plotting each chart.

write_presets.py generates the presets - its very hacked together at the moment, to add a new preset for a map it is suggested
to copy the code block for a different one (eg 'default') and alter the parameters as necessary. 
