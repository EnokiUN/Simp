
import requests
import urllib.parse

# api link: https://replit.com/@skellymclane386/vtuberapi#main.py

class API:
  base = "https://vtuberapi.skellymclane386.repl.co"

  @classmethod
  def handle_response(cls, res):
    if res.status_code != 200:
      return None

    data = res.json()
    if type(data) == dict:
      if data['type'] is not None:
        return -1

    return data

  @classmethod
  def random(cls):
    res = requests.get(url=f"{cls.base}/random")
    return cls.handle_response(res)

  @classmethod
  def advrandom(cls, org: str = None):
    res = requests.get(url=f"{cls.base}/advrandom{'' if not org else f'?org={org}'}")
    return cls.handle_response(res)

  @classmethod
  def org(cls):
    res = requests.get(url=f"{cls.base}/org")
    return cls.handle_response(res)

  @classmethod
  def get_org(cls, org: str):
    res = requests.get(url=f"{cls.base}/org/{org}")
    return cls.handle_response(res)

  @classmethod
  def get_vtuber(cls, vtuber_id: str):
    res = requests.get(url=f"{cls.base}/vtubers/{vtuber_id}")
    return cls.handle_response(res)

  @classmethod
  def search(cls, name: str=None, en_name: str = None, org: str = None):
    query = {}
    if name is not None:
      query['name'] = name
    if en_name is not None:
      query['english_name'] = en_name
    if org is not None:
      query['org'] = org
    res = requests.get(url=f"{cls.base}/search?{urllib.parse.urlencode(query)}")
    return cls.handle_response(res)

print(API.search(name="sar"))
