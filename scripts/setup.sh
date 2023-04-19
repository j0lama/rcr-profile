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

# Generate RCR config file
if [ $# -eq 2 ]
then
    echo "network = {" > rcr.conf
    for i in {1..$2}
    do
        echo "    node$i = {" >> rcr.conf
        echo "        client_ip_addr = \"192.168.1.$i\";" >> rcr.conf
        echo "        internal_ip_addr = \"192.168.1.$i\";" >> rcr.conf
        echo "        internal_port = 20000;" >> rcr.conf
        echo "hashmap_size = 1000;" >> rcr.conf
        echo "    };" >> rcr.conf
    done
    echo "}" >> rcr.conf
fi

# Build client
cd  client/
make

# Build db_populator
cd db_populator/
make