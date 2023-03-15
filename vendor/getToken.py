from flask import request
import requests
import json

def getToken():
  url = "https://cads-api.fpt.vn/fiber-detection/v2/getToken"

  payload = json.dumps({
    "clientId": "H8J1NKema4LrrUu6TYq6kH5if1JX6UyQ",
    "clientSecret": "RimknsnMuXAzi6gzWqinaUyLMgS95tbp"
  })
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  return json.loads(response.text)


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

