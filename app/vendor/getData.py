import requests
import json
from datetime import datetime
from requests.adapters import HTTPAdapter, Retry

from app.extensions import cache


@cache.cached(timeout=1200)
def getData(token):
  # Tạo key duy nhất cho API endpoint dựa trên đường dẫn và thời gian tạo key
  cache_key = hash('cache_key') + hash(datetime.now())

    # Kiểm tra xem cache có chứa dữ liệu JSON hay không
  data = cache.get(cache_key)

    # Nếu không, lấy dữ liệu từ API và lưu trữ trong cache
  if not data:
      # Get data
    url = "https://cads-api.fpt.vn/fiber-detection/v2/using_json_inf/2022/12"

    payload = ""
    headers = {
      'Content-Type': 'application/json',
      'Authorization': token
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    # session = requests.Session()
    # retry = Retry(connect=2, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)

    # response = session.post(url, data=payload, headers=headers, verify=False)

    # data = response.json()

    cache.set(cache_key, data)
    print('Not cache')
  else:
      print('Cached')
  return data


