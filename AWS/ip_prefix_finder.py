#!/usr/bin/env python3
####################################################################################################################

# Developed by iosama.amin@gmail.com                                                                               #  

#                                                                                                                  #

# Version 1                                                                                                        #

#                                                                                                                  #

# This script finds you the IP of an AWS service in a specific region                                              #

#                                                                                                                  #

#                                                                                                                  #

####################################################################################################################

import argparse
import requests
import sys

#constantly update the list with the regions and services
region_choices = []
services_choices = []

try:
    response = requests.get(url="https://ip-ranges.amazonaws.com/ip-ranges.json", timeout=10)
    response.raise_for_status()
    json_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from AWS website https://ip-ranges.amazonaws.com/ip-ranges.json : {e}")
    sys.exit(1)

for key in json_data:
    if key == "prefixes":
        for entry in json_data[key]:
            if not entry['region'] in region_choices:
                region_choices.append(entry['region'])
            if not entry['service'] in services_choices:
                services_choices.append(entry['service'])


#Add the regions and the services to our script parameters 

parser = argparse.ArgumentParser(description="This script finds you the IP (ip_prefix) of an AWS service in a specific region")

parser.add_argument('-r', '--Region', help='Region name, for example: us-west-2, default: us-west-2', default='us-west-2',choices=region_choices)
parser.add_argument('-s', '--Service', help='Service, for example: EBS, EC2_INSTANCE_CONNECT', required=True, choices=services_choices)

arguments = parser.parse_args()
REGION = arguments.Region
SERVICE = arguments.Service

try:
    response = requests.get(url="https://ip-ranges.amazonaws.com/ip-ranges.json", timeout=10)
    response.raise_for_status()
    json_data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from AWS website https://ip-ranges.amazonaws.com/ip-ranges.json : {e}")
    sys.exit(1)

found = False

for key in json_data:
    if key == "prefixes":
        for entry in json_data[key]:
            if entry["region"] == REGION and entry["service"] == SERVICE:
                print(entry["ip_prefix"])
                found = True

if not found:
    print(f"No IP prefix found for service '{SERVICE}' in region '{REGION}'.")



