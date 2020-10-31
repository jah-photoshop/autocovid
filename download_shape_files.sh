#!/bin/bash

set -euo pipefail

cd data
# https://geoportal.statistics.gov.uk/datasets/middle-layer-super-output-areas-december-2011-boundaries-ew-bsc
if [ ! -f "Middle_Layer_Super_Output_Areas__December_2011__Boundaries_EW_BSC-shp.zip" ]; then
    curl --compressed -J -O "https://prod-hub-indexer.s3.amazonaws.com/files/87aa4eb6393644768a5f85929cc704c2/0/full/27700/87aa4eb6393644768a5f85929cc704c2_0_full_27700.zip"
fi

# https://geoportal.statistics.gov.uk/datasets/local-authority-districts-may-2020-boundaries-uk-bgc-1
if [ ! -f "Local_Authority_Districts__May_2020__Boundaries_UK_BGC-shp.zip" ]; then
    curl --compressed -J -O "https://prod-hub-indexer.s3.amazonaws.com/files/3b374840ce1b4160b85b8146b610cd0c/0/full/27700/3b374840ce1b4160b85b8146b610cd0c_0_full_27700.zip"
fi

# https://geoportal.statistics.gov.uk/datasets/major-towns-and-cities-december-2015-boundaries
if [ ! -f "Major_Towns_and_Cities__December_2015__Boundaries-shp.zip" ]; then
    curl --compressed -J -O "https://prod-hub-indexer.s3.amazonaws.com/files/58b0dfa605d5459b80bf08082999b27c/0/full/27700/58b0dfa605d5459b80bf08082999b27c_0_full_27700.zip"
fi