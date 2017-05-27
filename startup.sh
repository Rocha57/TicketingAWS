#!/bin/bash
sudo apt-get -y update
sudo apt-get -y install python3-pip
yes | pip3 install boto3
wget https://raw.githubusercontent.com/Rocha57/TicketingAWS/master/SQS/authentication.py
python3 authentication.py 