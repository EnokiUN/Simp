import json
from random import choice, choices, randint
from collections import Counter


def holodex_read():
  with open("./holodex.db", 'r') as r:
    data = json.load(r)
  return data

def list_filter(func, items):
  return [item for item in items if func(item) == True]

def list_find(func, items):
  for item in items:
    if func(item) == True:
      return item

def between(num: int, counter: Counter):
  val = min(list(counter.values()), key=lambda x:abs(x-num))
  return list_find(lambda value: value[1] == val, counter.items())[0]

class Data:
  def __init__(self):
    self.orgs = {}
    self._choices = []
    data = holodex_read()
    self.total = len(data)
    for i in data:
      if str(i['org']) not in self._choices:
        self.orgs[str(i['org'])] = []
        self._choices.append(str(i['org']))

      self.orgs[str(i['org'])].append(i['id'])

    self._chances = [(len(self.orgs[_choice]) / self.total) * 100 for _choice in self._choices]


  def random_org(self, inc: list):
    _chances = self._chances

    if len(inc) != 0:
      for i in inc:
        _chances[self._choices.index(i)] *= 2
    return choice(choices(self._choices, _chances, k=1000))

  def random_vtuber(self, orgs: list = [], vtubers=[]):
    _choices = self.orgs[self.random_org(orgs)]
    if any([i in _choices for i in list(set(vtubers))]):
      print('yes')
      _choices += vtubers
    else:
      print("no")
    return choice(_choices)

  def get_vtuber(self, vtuber_id):
    return list_find(lambda item: item['id'] == vtuber_id, holodex_read())


d = Data()

choosen = d.random_vtuber(['Independents']*10, ["UCaTUFB2QKcLDxdP3RcX3eFw"])
x = 0
while choosen != "UCaTUFB2QKcLDxdP3RcX3eFw":
  x += 1
  choosen = d.random_vtuber(['Independents']*10, ["UCaTUFB2QKcLDxdP3RcX3eFw"])


print(d.get_vtuber(choosen))
print(f"\n\nIterations: {x}")




