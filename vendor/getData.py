import requests
import json

def getData(token):
  url = "http://cads-api.fpt.vn/fiber-detection/v2/using_json_inf/2022/12"

  payload = ""
  headers = {
    'Content-Type': 'application/json',
    'Authorization': token
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  return json.loads(response.text)


