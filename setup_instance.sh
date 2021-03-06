#!/bin/bash
# Once the volume is mounted, gets pip and 
# installs all of packages needed for text_sim.py
# Also installs sqlite3 and unzip for old project
# EC2 setup
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo python3 -m pip install --upgrade numpy
sudo python3 -m pip install --upgrade scipy
sudo python3 -m pip install --upgrade gensim
sudo python3 -m pip install --upgrade networkx
sudo python3 -m pip install --upgrade IPython
sudo apt-get update
sudo apt-get install unzip
sudo apt-get install sqlite3
sudo apt-get install git
