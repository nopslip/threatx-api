### Basic example of ThreatX API script 

This is a basic example of how to interact with the ThreatX API using Python. This example contains a call to the metrics per hour endpoint. Please see the ThreatX API guide for full details on other endpoints: [support.threatx.com/hc/en-us/articles/360000661851-API-Reference-Guide](https://support.threatx.com/hc/en-us/articles/360000661851-API-Reference-Guide)

#### Setup 

1) Setup your python virtual env

`python3 -m venv base_env`

2) Activate your venv

`source /base_env/bin/activate`

3) Install packages. For this example it's simply requests

`pip install requirements.txt` 

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

 