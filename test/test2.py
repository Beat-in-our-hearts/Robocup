# encoding:utf-8
import requests

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=1Gw70VWpThVjsfwc8myFBuA5&client_secret=pdbxFfZ94LzQD988L4TzGuY8iy0uqFkc'
response = requests.get(host)
# if response:
print(response.json()["access_token"])
