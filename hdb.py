
from typing import Any, Union
from dotenv import load_dotenv
import os

from src.holodex import HoloDex
load_dotenv()
from pymongo import MongoClient
import json
from discord.utils import find as list_find
from pyjarowinkler.distance import get_jaro_distance
from random import choice, choices, randint
from collections import Counter, namedtuple

client = MongoClient(os.getenv("URI"))

db = client.get_database("Simp")

users = db.get_collection("users")
cards = db.get_collection("cards")

Rarity = namedtuple("Rarity", ["name", 'value', 'chance'])


def closest(num: int, counter: Counter):
  curr = ("COMMON", counter.get("COMMON", 0))
  for key, value in counter.items():
    if abs(num - value) < abs(num - curr[1]):
      curr = (key, value)
  return RarityData.from_name(curr[0])


class RarityData:

  @staticmethod
  def read() -> Union[dict[str, Any], list[str]]:
    with open('./rarity.json', 'r') as r:
      data = json.load(r)
    return data

  @staticmethod
  def from_name(name: str):
    """Finds the rarity by name and returns it as a namedtuple

    Args:
        name (str): the name of the rarity

    Returns:
        Rarity: Rarity(name=str, value=int, chance=float)
    """
    return Rarity(*list_find(lambda rarity: rarity[0] == name, RarityData.read()["data"].values()))

  @staticmethod
  def from_value(value: int):
    """Finds the rarity by value and returns it as a namedtuple

    Args:
        value (int): the value identity of the rarity

    Returns:
        Rarity: Rarity(name=str, value=int, chance=float)
    """
    return Rarity(*list_find(lambda rarity: rarity[1] == value, RarityData.read()["data"].values()))

  @classmethod
  def CHANCES(cls) -> list[float]:
    """gets the rarity chance of each rarity class

    Returns:
        list[float]: list containing the chance for each rarity class
    """
    return [v[2] * 0.5 for v in cls.VALUES().values()]

  @classmethod
  def CHOICES(cls) -> list[str]:
    """gets all class names as a list

    Returns:
        list: list containing rarity class names
    """
    return [v[0] for v in cls.VALUES().values()]

  @classmethod
  def VALUES(cls) -> dict[str, Rarity]:
    """just takes the data from the json and turns it into a dictionary

    Returns:
        [type]: [description]
    """
    return {key:Rarity(*value)  for key, value in cls.read()['data'].items()}


  @classmethod
  def random(cls):
    _choices = cls.CHOICES()
    _chances = cls.CHANCES()
    # print(_choices)
    # print(_chances)
    counter = Counter(choices(_choices,_chances,k=1000))
    number = randint(0, 1000)
    # print(f"Num: {number}")
    return closest(
      num=number,
      counter=counter
    )



class VtuberEntry:
  keys = ["id", "name", "english_name", "type", 'org', "group", "photo", "twitter", "video_count", "sub_count", "clip_count", "top_topics"]
  def __init__(self, **data):
    self.id: str = None
    self.name: str = None
    self.english_name: str = None
    self.type: str = None
    self.org: str = None
    self.group: str = None
    self.photo: str = None
    self.twitter: str = None
    self.video_count: str = None
    self.subscriber_count: str = 0
    self.clip_count: str = None
    self.top_topics: list[str]

    for key in data.keys():
      setattr(self, key, data[key])

  def __repr__(self) -> str:
    return f"Entry(id={self.id}, name={self.name}, org={self.org})"

  def out(self) -> dict:
    return {i:getattr(self, i) for i in VtuberEntry.keys}

  @property
  def sub_count(self):
    res = self.subscriber_count
    return (0 if not res else res)

  @staticmethod
  def get(vtuber_id: str):
    return VtuberEntry(**list_find(lambda vtuber: vtuber['id'] == vtuber_id, Data.holodex_read()))

  @staticmethod
  def random():
    return VtuberEntry(**choice(Data.holodex_read()))

  def copy(self):
    return VtuberEntry(**self.out())




class Data:
  DEX = HoloDex()

  @staticmethod
  def holodex_read():
    with open("./holodex.db", 'r') as r:
      data = json.load(r)
    return data

  @staticmethod
  def get_vtuber(vtuber_id: str):
    data = Data.holodex_read()
    return list_find(lambda vtuber: vtuber['id'] == vtuber_id, data)

  @staticmethod
  def find_by_name(query: str):
    res = Data.DEX.autocomplete_result(query)
    data = res.json()
    return data[0]



class Card:
  def __init__(self, card_id: int):
    self.card_id = card_id
    self.raw = {}
    self.raw = self.get_data()

  @property
  def exists(self):
    return self.raw is not None


  @property
  def query(self):
    return { "card_id": self.card_id }


  @property
  def cost(self):
    vtuber = self.vtuber.copy()
    rarity_value = (1 - self.rarity_data.chance / sum(RarityData.CHANCES()))
    return int(vtuber.sub_count) * rarity_value

  @property
  def vtuber_id(self):
    return self.raw['vtuber_id']
  @property
  def vtuber(self) -> VtuberEntry:
    return VtuberEntry.get(self.raw['vtuber_id'])
  @property
  def rarity(self):
    return self.raw['rarity']
  @property
  def rarity_data(self):
    return RarityData.from_value(self.raw['rarity'])
  @property
  def xp(self):
    return self.raw['xp']
  @property
  def owner(self):
    return self.raw['owner']

  def get_data(self):
    return cards.find_one(self.query)

  def update(self, data: dict):
    cards.update_one(self.query, data)
    self.raw = self.get_data()


  def inc_xp(self, amount: float):
    self.update({"$inc": { "xp": amount }})

  @staticmethod
  def create(owner: int, vtuber_id: str, rarity: int) -> int:
    card_id = cards.count_documents({})
    cards.insert_one({
      "owner": owner,
      "vtuber_id": vtuber_id,
      "xp": 0.0,
      "rarity": rarity,
      "card_id": card_id
    })
    return card_id

  @classmethod
  def from_card_id(cls, card_id: int):
    return Card(card_id)

class User:
  def __init__(self, user_id: int):
    self.user_id: int = user_id
    self.raw = {}
    self.init()


  def init(self):
    if not self.get_data():
      users.insert_one({
        "user_id": self.user_id,
        "prefixs": [],
        "bal": 0.0
      })
    self.raw = self.get_data()
    self.raw['cards'] = [card['card_id'] for card in cards.find({ "owner": self.user_id })]


  @property
  def prefixs(self):
    return self.raw["prefixs"]

  @property
  def cards(self):
    return self.raw['cards']

  @property
  def bal(self) -> float:
    return self.raw['bal']

  def get_card(self, card_id: int):
    return Card(card_id)

  def sell_card(self, card_id: int):
    card = Card(card_id)
    if not card.exists:
      return 1
    elif card.owner == self.user_id:
      cards.delete_one({ "card_id": card_id })
      self.update({"$inc":{"bal": card.cost }})
      return card
    else:
      return 0

  @property
  def query(self):
    return { "user_id": self.user_id }

  def get_data(self):
    return users.find_one(self.query)

  def update(self, data: dict):
    users.update_one(self.query, data)
    self.raw = self.get_data()
    self.raw['cards'] = [card['card_id'] for card in cards.find({ "owner": self.user_id })]




