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

def between(num: int, counter):
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
    return between(randint(0, 1000), Counter(choices(self._choices, _chances, k=1000)))

  def random_vtuber(self, orgs: list = [], vtubers=[]):
    _choices: list = self.orgs[self.random_org(orgs)]
    if any([i in _choices for i in list(set(vtubers))]):
      print('yes')
      _choices += vtubers
    else:
      print("no")
    total = len(_choices)
    _chances = [(1 / total) * 100] * total

    if len(vtubers) != 0:
      for i in vtubers:
        if i in _choices:
          _chances[_choices.index(i)] *= 2

    return between(randint(0, total), Counter(choices(_choices, _chances, k=total)))

  def get_vtuber(self, vtuber_id):
    return list_find(lambda item: item['id'] == vtuber_id, holodex_read())

class Data2:
  def __init__(self):

    self.org_increase = 0.5
    self.vtube_increase = 0.5


    self.orgs = {}
    self.org_names = []
    self.vtubers: list = []
    data: list = holodex_read()
    for i in data:
      org_name: str = str(i['org'])
      self.vtubers.append((i['id'], org_name))

      if org_name not in self.org_names:
        self.org_names.append(org_name)
        self.orgs[org_name] = []
      self.orgs[org_name].append(i)
    self.total_vtubers = len(self.vtubers)
    self.total_orgs = len(self.orgs)

  def vtuber_ids(self) -> list:
    return [i[0] for i in self.vtubers]

  def vtuber_chances(self) -> list:
    return ([(1 / self.total_vtubers) * 100] * self.total_vtubers)


  def get_vtubers_with_org(self, vtubers: list, orgs: list) -> list:
    _options = []
    for org in orgs:
      _options += [i for i in self.orgs[org] if i['id'] in vtubers]
    return _options


  def random_vtuber(self, orgs=[], vtubers=[]):
    _choices = self.vtuber_ids()
    _chances = self.vtuber_chances()

    for org in orgs:
      if org in self.org_names:
        for vtuber in self.orgs[org]:
          _chances[_choices.index(vtuber['id'])] *= 1 + self.org_increase

    for vtuber in vtubers:
      if vtuber in _choices:
        _chances[_choices.index(vtuber)] += self.vtube_increase

    counter = Counter(choices(_choices, _chances, k=self.total_vtubers))
    num = randint(0, 1000)
    return between(num, counter)

  def get_vtuber(self, vtuber_id: str):
    return list_find(lambda item: item['id'] == vtuber_id, holodex_read())


d = Data2()

res = d.random_vtuber(['Independents']*10, ["UCaTUFB2QKcLDxdP3RcX3eFw"]*10)
x = 0
while res != 'UCaTUFB2QKcLDxdP3RcX3eFw':
  x += 1
  res = d.random_vtuber(['Independents']*10, ["UCaTUFB2QKcLDxdP3RcX3eFw"]*10)


print(d.get_vtuber(res))
print(f"Iterations: {x}")
