### Basic example of ThreatX API script 

This is a basic example of how to interact with the ThreatX API using Python. This example contains a call to the metrics per hour endpoint. Please see the ThreatX API guide for full details on other endpoints: [support.threatx.com/hc/en-us/articles/360000661851-API-Reference-Guide](https://support.threatx.com/hc/en-us/articles/360000661851-API-Reference-Guide)

#### Setup 

1) Setup your python virtual env

`python3 -m venv base_env`

2) Activate your venv

`source /base_env/bin/activate`

3) Install packages. For this example it's simply requests

`pip install -r requirements.txt` 

4) Run the script 

`python threatx_api_base.py` 


Output will look something like this:

```
[{'blocks': 34, 'timestamp': 1591326000, 'total': 2523},
 {'blocks': 0, 'timestamp': 1591340400, 'total': 3323},
 {'blocks': 3, 'timestamp': 1591351200, 'total': 4223},
 {'blocks': 0, 'timestamp': 1591354800, 'total': 2023},
 {'blocks': 24, 'timestamp': 1591358400, 'total': 1353},
 {'blocks': 1, 'timestamp': 1591362000, 'total': 2372}]
 ```

 #### Bulk Sites 
 The bulk_sites.py can be used to to bulk add and update sites in ThreatX. 

 1) Set your API key as a environmental variable

 ` export TX_API_KEY="your_api_key"`

 2) In the script, set the `customer_name` variable
 ```
 # what customer are we adding sites for?
customer_name = 'your_customer_name_here'
``` 
3) Add the sites you want to add or update to bulk_sites.csv. Script currently pulls in `hostname` and `backend/origin` but it can easily be updated to included other vaules like SSL_BLOB.  

4) You can also adjust other values (blocking modes, etc) directly in the `new_site` and `update_site` variables. For example, if you want to adjust blocking modes for new sites just adjust this accordingly. If all values aren't static across all new sites you can add then to the CSV file and import them accordingly. 

```    
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

