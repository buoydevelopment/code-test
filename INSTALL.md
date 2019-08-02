# Code Challenge for BuoyDevelopment by Mauricio Bergallo

## Description

The API in this repo is used to shorten urls. Is an API created in Python 3 with Flask Framework; the Application uses a Database SQLite.

## PreRequisites

- Virtual Environment should be installed and active
- To Activate in Windows ``` λ venv\Scripts\activate.bat ```; in Unix / MacOS ```$ source ./env/bin/activate```
- Install Dependencies ```$ pip install -r .\requirements.txt```

## Steps to Run Locally

- Set the Environment Variable: ``` λ set APP_SETTINGS=src.config.LocalConfig ``` (Windows) ``` $ export APP_SETTINGS=src.config.LocalConfig ```
- Start the Server: ``` py manage.py run ```
- Test:
``` 
curl -X POST \
  http://localhost:5000/urls \
  -H 'Content-Type: application/json' \
  -d '{
	"url": "http://example.com",
	"code": "Ncr8p7"
}'
```

## Steps to Run Unit Test
- Execute the Test: ``` py manage.py test ```