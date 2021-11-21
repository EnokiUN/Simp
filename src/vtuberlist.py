import requests

# source: https://vdb.vtbs.moe


# VtuberEntry response data
# {'uuid': '9b44e2a9-3334-5792-b57d-1bf0939afe49', 'type': 'vtuber', 'bot': False, 'accounts': [
#   {'id': '5450477', 'type': 'official', 'platform': 'bilibili'}],
#   'name': {'extra': [], 'cn': '-可乐KORA-', 'default': 'cn'}, 'group': 'ee2d6579-f7b2-59e4-be05-ca88f4bdff7d'}

class VtuberEntry:
  def __init__(self) -> None:
    self.uuid: str = None
    self.type: str = None
    self.bot: bool = False
    self.accounts = []
    self.name = { "extra": [], "cn": None, "default": "cn"}
    self.group: str = None

class VtuberList:
  def __init__(self):
    self.url = "https://vdb.vtbs.moe/json/list.json"
    self.raw = {}
    self.vtbs = []
    self.meta = {}

    self.update()


  def update(self):
    res = requests.get(self.url)
    self.raw = res.json()
    self.meta = self.raw["meta"]
    self.vtbs = self.raw["vtbs"]

v = VtuberList()

print(v.meta)
print(v.vtbs[0])
