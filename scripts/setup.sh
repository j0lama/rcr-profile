#!/bin/bash

cd /local/

# Install dependencies
sudo apt update -y
sudo apt install -y libconfig-dev

# Clone RCR repository
git clone https://j0lama:$1@github.com/j0lama/rcr.git

# Build RCR node
cd rcr/
make

# Build client
cd  client/
make

# Build db_populator
cd db_populator/
make