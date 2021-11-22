import json
from flask import Flask, request
from pyjarowinkler.distance import get_jaro_distance as jaro
import config
import threading
from random import choice, choices, randint
from collections import Counter

app = Flask("Vtuber API")

def holodex_read():
  with open("./holodex.db", 'r') as r:
    data = json.load(r)
  return data

### init data
data = holodex_read()
vtubers = []
vtuber_ids = []

orgs = {}
org_names = []

for i in data:
  vtuber_ids.append(i['id'])
  vtubers.append(i)
  org_name = str(i['org'])
  if org_name not in org_names:
    org_names.append(org_name)
    orgs[i['org']] = []
  orgs[i['org']].append(i)

total_orgs = len(org_names)
total_vtubers = len(vtuber_ids)


# helper functions
def list_filter(func, items):
  return [item for item in items if func(item) == True]

def list_find(func, items):
  for item in items:
    if func(item) == True:
      return item

def between(num: int, counter):
  val = min(list(counter.values()), key=lambda x:abs(x-num))
  return list_find(lambda value: value[1] == val, counter.items())[0]

def _get_vtuber(vtuber_id: str):
  return list_find(lambda item: item['id'] == vtuber_id, data)

# routes

@app.route("/vtubers")
def vtubers():
  return json.dumps(data)

@app.route('/vtubers/<vtuber_id>')
def get_vtuber(vtuber_id=None):
  if not vtuber_id:
    return json.dumps({
      "type": "error",
      "message": "No Id Specified"
    })
  else:
    res = list_find(lambda item: item['id'] == vtuber_id, data)
    if not res:
      return {
        "type": "error",
        "message": "no vtuber with that id found"
        }
    else:
      return json.dumps(res)


jaro_options = dict(
  winkler=True, scaling=0.1
)

name_thresh = 0.85

@app.route("/search")
def search():
  out = []

  query_keys = list(request.args.keys())

  for i in data:
    ok = True
    if "name" in query_keys:
      name = str(request.args.get("name"))
      value = jaro(name, i['name'], **jaro_options)
      if value < config.name_thresh and not i['name'].lower().startswith(name.lower()):
        ok = False
        continue
    if "english_name" in query_keys:
      value = jaro(i['english_name'], request.args.get("english_name"), **jaro_options)
      if value < config.name_english_thresh:
        ok=False
        continue
    if "org" in query_keys:
      org = str(request.args.get("org"))
      if str(i['org']) != org:
        ok = False
        continue
    if ok is True:
      out.append(i)

  return json.dumps(out)


@app.route("/random")
def random_vtuber():
  return json.dumps(choice(data))

@app.route("/advrandom", methods=["get"])
def adv_random_vtuber():
    org = request.args.get("org", default=None)
    _choices = vtuber_ids
    _chances = [(1 / total_vtubers) * 100] * total_vtubers


    if org is not None:
      if org in orgs.keys():
        for vtuber in orgs[org]:
          _chances[_choices.index(vtuber['id'])] *= 1 + config.org_increase
      else:
        return json.dumps({
          "type": "error",
          "message": f"that org doesn't exist Options: {list(orgs.keys())}"
        })

    counter = Counter(choices(_choices, _chances, k=1000))
    num = randint(0, 1000)
    return json.dumps(_get_vtuber(between(num, counter)))

@app.route('/org')
def _org():
  return json.dumps(orgs)

@app.route("/org/<org>")
def _org_get(org: str = None):
  if not org:
    return json.dumps({"type": "error", "message": "invalid org"})
  if org not in org_names:
    return json.dumps({"type": "error", "message": "no org with that name exists"})

  return json.dumps(orgs[org])

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

def run():
  app.run(
    host="0.0.0.0",
    port=3000,
    debug=True
  )



if __name__ == "__main__":
  run()
