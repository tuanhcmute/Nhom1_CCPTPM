from flask import request
import requests
import json
from requests.adapters import HTTPAdapter, Retry

def getToken():
  url = "https://cads-api.fpt.vn/fiber-detection/v2/getToken"

  payload = json.dumps({
    "clientId": "H8J1NKema4LrrUu6TYq6kH5if1JX6UyQ",
    "clientSecret": "RimknsnMuXAzi6gzWqinaUyLMgS95tbp"
  })
  headers = {
    'Content-Type': 'application/json'
  }


  session = requests.Session()
  retry = Retry(connect=3, backoff_factor=0.5)
  adapter = HTTPAdapter(max_retries=retry)
  session.mount('http://', adapter)
  session.mount('https://', adapter)

  response = session.post(url, data=payload, headers=headers, verify=False)

  parsed = response.json()

  return parsed



def refreshToken(response):
  try:
    token = request.cookies.get('access_token')
    if token is None:
        tokenDic = getToken()
        accessToken, maxAge = tokenDic['access_token'], tokenDic['expires_in']
        response.set_cookie('access_token', accessToken, max_age=10)
    return response
  except (RuntimeError, KeyError):
    return response

