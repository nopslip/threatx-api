import requests
import json
import csv
import logging
import os
from pprint import pprint 

# what customer are we adding sites for?
customer_name = 'your_customer_name_here'

# enable logging. This will log key events to local file 
logging.basicConfig(filename='tx-bulk-site.log',
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

# API Endpoints
login_endpoint = "https://provision.threatx.io/tx_api/v1/login"
sites_endpoint = "https://provision.threatx.io/tx_api/v2/sites"

# Define Input Variables
bulk_sites_file = csv.reader(open('bulk_sites.csv'))

# This function uses your TX API KEY to get a token 
def api_login_pull():
    '''function used to get TX-API token. Tokens expire after ~30 mins.'''
    logger.info("-->Getting TX-API token")
    query = {"api_token": tx_api_key,"command": "login"} # craft login query 
    try:
        login_resp = requests.post(login_endpoint, json=query).json() # hit the API, save the response 
    except requests.exceptions.RequestException as e: 
        logger.error(f"Error connecting to TX-API to pull token: {e}")
        return False
    return login_resp['Ok']['token'] # return the token 

# Add A Site to a Customer
def add_site(_site_name, _backend):
    '''This function will add a new site to ThreatX'''

    # get a new token for each call 
    threatx_token = api_login_pull()

    new_site = { 
        "command":"new", 
        "token":threatx_token, 
        "customer_name":customer_name, 
        "site":{ "hostname":_site_name, 
        "backend":[[_backend,True]],
         "isEnabled":True, 
         "request_blocking":False, 
         "risk_based_blocking":False,
         "manual_action_blocking":True
         } 
    }

    # hit the API, save the response 
    try:
        resp = requests.post(sites_endpoint, json=new_site)
        print(resp.text)
    except requests.exceptions.RequestException as e:  
        logger.error(f"Error connecting to TX-API! {e}")
        return False 

    json_resp = resp.json()

    return json_resp

def update_site(_site_name, _backend):
    '''This function will update existing sites in ThreatX'''
    
     # get a new token for each call 
    threatx_token = api_login_pull()
    
    # basic example 
    update_site = { 
        "command":"update", 
        "token":threatx_token, 
        "customer_name":customer_name,
        "name":_site_name, 
        "site":{ "hostname":_site_name, 
        "backend":[[_backend,True]],
         "isEnabled":True, 
         "request_blocking":False, 
         "risk_based_blocking":False,
         "manual_action_blocking":True
         } 
    }

    # hit the API, save the response 
    try:
        resp = requests.post(sites_endpoint, json=update_site)
        print(resp.text)
    except requests.exceptions.RequestException as e:  
        logger.error(f"Error connecting to TX-API! {e}")
        return False 

    json_resp = resp.json()

    return json_resp


# Loop through rows in CSV and create sites in ThreatX, one per line in the CSV
for site in bulk_sites_file:
    site_name = site[0]
    backend = site[1]
 
    # to add sites: 
    # add_site(site_name, backend)

    # to update sites
    update_site(site_name, backend)