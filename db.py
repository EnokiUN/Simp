
from random import random, randint, choice, choices
import pymongo
import os
from collections import Counter, namedtuple
from database import get_randoms, read as holodex_read
import discord
from pyjarowinkler.distance import get_jaro_distance


from src.holodex import Entry

client = pymongo.MongoClient(os.getenv("URI"))
db = client.get_database("Simp")

users = db.get_collection("users")

characters = "1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"

def random_id(length=10):
  return "".join([choice(characters) for i in range(length)])


def closest(num: int, counter: Counter):
  curr = ("COMMON", counter.get("COMMON"))
  for key, value in counter.items():
    if abs(num - value) < abs(num - curr[1]):
      curr = (key, value)
  return curr


Rarity = namedtuple("Rarity", ['name', 'value', "chance"])

class RARITY:
  COMMON=Rarity("COMMON", value=1, chance=74.3)
  UNCOMMON=Rarity("UNCOMMON", value=2, chance=55)
  RARE=Rarity("RARE", value=3, chance=35)
  SUPER_RARE=Rarity("SUPER_RARE", value=4, chance=15)
  ULTRA_RARE=Rarity("ULTRA_RARE", value=5, chance=10)
  LEGENDARY=Rarity("LEGENDARY", value=6, chance=7)
  MYTHIC=Rarity("MYTHIC", value=7, chance=3)
  WAIFU=Rarity("WAIFU", value=8, chance=0.7)
  FRIEND=Rarity("Friend", value=9, chance=0.01)
  CHOICES=["COMMON", "UNCOMMON", "RARE", "SUPER_RARE", "ULTRA_RARE", "LEGENDARY", "MYTHIC", "WAIFU", "FRIEND"]
  CHANCES=[i*0.5 for i in [  74.3,    55,    35,     15,     10,     7,     3,     0.7,    0.01  ]]

  @staticmethod
  def get(value: int):
    print(value)
    for key in RARITY.CHOICES:
      v = getattr(RARITY, key)
      if v.value == value:
        return v
    return RARITY.COMMON

  @staticmethod
  def random():
    results = choices(RARITY.CHOICES,RARITY.CHANCES,k=1000)
    chances = Counter(results)
    chance = randint(0, 1000)
    return closest(chance, chances)


class Card:
  def __init__(self, **kwargs) -> None:
    self.card_id: int = None
    self.owner: int = None
    self.vtuber_id: str = None
    self.xp = 0
    self.rarity: Rarity = Rarity("None", -1, -1)

    for key in kwargs:
      if key == "rarity":
        self.rarity = RARITY.get(kwargs[key])
      else:
        setattr(self, key, kwargs[key])

  def out(self):
    return { "card_id": self.card_id, "owner": self.owner, "vtuber_id": self.vtuber_id, "xp": self.xp, "rarity": self.rarity.value }

  @staticmethod
  def from_data(data: dict):
    return Card(**data)

  @staticmethod
  def generate(vtuber_id: str, owner: int):
    return Card(
      owner=owner,
      card_id=f"{owner}{random_id(5)}",
      vtuber_id=vtuber_id,
      xp=0,
      rarity=RARITY.random()
    )

  @staticmethod
  def get_vtuber(vtuber_id: str) -> Entry:

    return Entry(**discord.utils.find(lambda vtuber: vtuber['id'] == vtuber_id, holodex_read()))

async def create_user(user_id: int):
  return users.insert_one({
    "user_id": user_id,
    "cards": [],
    "prefixs": [],
    "bal": 0
  })


async def get_user(user_id: int):
  res = users.find_one({ "user_id": user_id })
  if not res:
    res = await create_user(user_id)
  return res

async def add_card(user_id: int, card: Card):
  return users.update_one({ "user_id": user_id },{
    "$push": {
      "cards": card.out()
    }
  })

async def find_vtuber(query: str, _min=0.8):
  out = []
  for entry in holodex_read():
    if get_jaro_distance(entry['name'], query) >= _min:
      out.append(entry)
  return [Entry(**x) for x in out]


async def sell_card(user_id: int, card_id: int):
  return users.update_one({ "user_id": user_id }, {
    "$pull": {
      "cards": { "card_id": card_id }
    }
  })



