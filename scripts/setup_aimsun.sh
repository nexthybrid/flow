#!/bin/bash

# create the conda environment
# conda create -y -n aimsun_flow python=2.7.4 # Anaconda library doesn't have this version of python 2.7.4, changed to 2.7 to try
conda create -y -n aimsun_flow python=2.7

# install numpy within the environment
source activate aimsun_flow
pip install numpy
