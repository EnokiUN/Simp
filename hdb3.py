
import pymongo
import os
from dotenv import load_dotenv
load_dotenv()
from random import choice, randint, choices
from collections import Counter
import json

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


def closest(num: int, counter: Counter):
  curr = ("COMMON", counter.get("COMMON", 0))
  for key, value in counter.items():
    if abs(num - value) < abs(num - curr[1]):
      curr = (key, value)
  return Rarity.get_name(curr[0])


class Rarity:
  values = [
    ("COMMON", 1, 74.3),
    ("UNCOMMON", 2, 55),
    ("RARE", 3, 35),
    ("SUPER_RARE", 4, 15),
    ("ULTRA_RARE", 5, 10),
    ("LEGENDARY", 6, 7),
    ("MYTHIC", 7, 3),
    ("WAIFU", 9, 0.01),
    ("FRIEND", 8, 0.7)
  ]

  @classmethod
  def get_name(cls, name: str) -> tuple:
    return list_find(lambda item: item[0] == name.upper(), cls.values)

  @classmethod
  def get_value(cls, value: int) -> tuple:
    return list_find(lambda item: item[1] == value, cls.values)

  @classmethod
  def random(cls):
    _choices = []
    _chances = []
    for choice, _, chance in cls.values:
      _choices.append(choice)
      _chances.append(chance)
    counter = Counter(choices(_choices,_chances,k=1000))
    number = randint(0, 1000)
    # print(f"Num: {number}")
    return closest(
      num=number,
      counter=counter
    )


class CardCounter:
  @classmethod
  def read(cls):
    with open("./count.txt", 'r') as r:
      data = int(r.read())
    return data

  @classmethod
  def write(cls, value: int):
    with open("./count.txt", 'w') as r:
      r.write(str(value))

  @classmethod
  def incriment(cls) -> int:
    val = cls.read()
    cls.write(val + 1)
    return val

client = pymongo.MongoClient(os.environ['URI'])

db = client.get_database("Simp")

users3 = db.get_collection("users3")
cards3 = db.get_collection("cards3")

async def create_card(owner: str):
  await init_user(owner)
  vtuber = choice(holodex_read())
  rarity = Rarity.random()
  card_id = CardCounter.incriment()
  card = {
    "owner": owner,
    "xp": 0,
    "rarity": rarity[1],
    "card_id": card_id
  }
  await add_card(owner, vtuber['id'], card_id, rarity[1], 0)
  return vtuber, rarity, card

async def add_card(owner: str, vtuber_id: str, card_id: str, rarity: int, xp: int):
  return cards3.insert_one({
    "owner": owner,
    "rarity": rarity,
    "xp": xp,
    "card_id": card_id,
    "vtuber_id": vtuber_id
  })

async def remove_card(card_id: str):
  return cards3.delete_one({"card_id": card_id})

async def get_card(card_id: str):
  return cards3.find_one({"card_id": card_id})

async def get_user(user_id):
  res = users3.find_one({"user_id": user_id})
  if not res:
    res = await create_user(user_id)
  return res

async def init_user(user_id: str):
  res = await get_user(user_id)
  if not res:
    await create_user(user_id)

async def create_user(user_id):
  return users3.insert_one({
    "user_id": user_id,
    "effects": [],
    "inv": [],
    "bal": 0,
    "cooldowns": {}
  })

async def fix_user(user_id):
  res = users3.find_one({"user_id":user_id})
  out = {"user_id":user_id}
  if not res['cooldowns']:
    out['cooldowns'] = {}
  if not res['bal']:
    out['bal'] = 0
  if not res['inv']:
    out['inv'] = []
  if not res['effects']:
    out['effects'] = []
  res = users3.update_one({"user_id":user_id}, { "$set": out })
  return res

async def inc_bal(user_id: int, amount: int):
  return users3.update_one({"user_id": user_id}, {"$inc": {"bal": amount} }).raw_result

async def get_user_cards(user_id):
  return [doc for doc in cards3.find({"owner":user_id})]

async def get_vtuber(vtuber_id: str):
  return list_find(lambda item: item['id'] == vtuber_id, holodex_read())

def get_cost(sub_count, rarity: tuple):
  return int(round(((int(sub_count) / 1000) * ((200 - rarity[2]) * 0.5)) * 114.02))


async def get_card_cost(card_id: int):
  card = await get_card(card_id)
  vtuber = await get_vtuber(card['vtuber_id'])
  cost = get_cost(vtuber['subscriber_count'], Rarity.get_value(card['rarity']))
  return cost, card, vtuber


