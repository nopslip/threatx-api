import requests 
import json
import logging
import os
from pprint import pprint
import time
import random
import string
import csv

# this is a generic base script for interacting with the ThreatX API
# Full ThreatX API reference can be found here
# https://support.threatx.com/hc/en-us/articles/360000661851-API-Reference-Guide

# customer name, all lowercase:  
customer_name = 'selab'

# metrics endpoint requires start and end unix times 
time_end = int(time.time()) # now 
time_start = time_end - (60 * 60 * 12) # 12 hours 

# API Endpoints used in this script (add more as necessary)
login_endpoint = "https://provision.threatx.io/tx_api/v1/login"
metrics_endpoint = "https://provision.threatx.io/tx_api/v1/metrics"

# enable logging. This will log key events to local file 
logging.basicConfig(filename='tx-api.log',
                    filemode='a',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# set your API key as an environmental variable in your shell, for example
# export TX_API_KEY="your_TX_API_KEY_GOES_HERE"
if 'TX_API_KEY' in os.environ:
    tx_api_key = os.environ['TX_API_KEY']
else:
    logger.exception('TX_API_KEY not set! This is required to run the script!')
    exit()

# This function uses your TX API KEY to get a token 
def api_login_pull():
    '''function used to get TX-API token. Tokens expire after ~30 mins.'''
    logger.info(f"-->Getting TX-API token")
    query = {"api_token": tx_api_key,"command": "login"} # craft login query 
    login_resp = requests.post(login_endpoint, json=query).json() # hit the API, save the response 
    return login_resp['Ok']['token'] # return the token 

def get_request_stats_by_hour():
    '''This function lists request statistics, including request count and blocked request count, 
    exposed as a timeseries data set. Data in this endpoint is aggregated to an hourly resolution.
    '''
    # craft query/payload 
    query = {
        "token": token,
        "command": "request_stats_by_hour",
        "customer_name": customer_name,
        "time_start": time_start,
        "time_end": time_end
    }
    
    # hit the API, save the response 
    resp = requests.post(metrics_endpoint, json=query)

    json_resp = resp.json()

    if resp.status_code == 200:
        result = json_resp['Ok']
        logger.info(f"Successfully recieved records for {customer_name} from {metrics_endpoint}!")
        return result
    else:
        logger.warning(f"Non 200 status coded returned from TX API. Got: {resp.status_code}")
        pprint(resp.json())
        result = False
        exit() # lets just exit the script if we get non 200 response from TX API 

# get our token 
token = api_login_pull()

# make a request to the metrics API
metrics = get_request_stats_by_hour()

# print our response 
pprint(metrics)












