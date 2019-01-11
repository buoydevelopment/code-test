import requests
import json

payload = {'url': "http://www.osmin.com", 'code': "12345"}

url = 'http://127.0.0.1:8000/api/v1/shorturl/'
headers = {
    'Authorization': 'Token 5fb1ac6ffc159dcfc5efe6ef95ae11ad0d849e62',
    'content-type': "application/json"}
response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
print(response.text)
#rp = response.json()

#response = requests.request("GET", url, headers=headers)
#print("GET:",response.text)
