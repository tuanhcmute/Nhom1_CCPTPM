import requests
import json
from datetime import datetime

from app.extensions import cache


# @cache.cached(timeout=1200)
def getData(token, month, year):
  # Tạo key duy nhất cho API endpoint dựa trên đường dẫn và thời gian tạo key
  # cache_key = hash('cache_key') + hash(datetime.now())

  #   # Kiểm tra xem cache có chứa dữ liệu JSON hay không
  # data = cache.get(cache_key)
  # monthCache = cache.get('month')
  # yearCache = cache.get('year')


  # if data and monthCache == month and year == yearCache:
  #   print('Cached')
  #   return data

  # Nếu không, lấy dữ liệu từ API và lưu trữ trong cache
  # Get data
  url = "https://cads-api.fpt.vn/fiber-detection/v2/using_json_inf/" + str(year) + "/" + str(month)
  payload = ""
  headers = {
    'Content-Type': 'application/json',
    'Authorization': token
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  data = json.loads(response.text)

  # cache.set(cache_key, data)
  # cache.set('month', month)
  # cache.set('year', year)
  print('Not cache')
  return data

