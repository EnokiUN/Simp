
import json
from src.holodex import Entry, HoloDex, ORGS
from random import choice
from collections import namedtuple

class VtuberEntry:
  def __init__(self, **data):
    self.name: str = None
    self.org: str = None

    self.photo: str = None

    self.attack: int = 0
    self.defense: int = 0
    self.speed: int = 0

    self.health: int = 0
    self.stamina: int = 0
    self.stamina_regen: int = 0
    self.mana: int = 0
    self.mana_regen: int = 0

    self.abilities = []
    self.card_id: int = 0

    for key in data.keys():
      setattr(self, key, data[key])

  def out(self):
    return {
      "name": self.name,
      "org": self.org,
      "photo": self.photo,
      "attack": self.attack,
      "defense": self.defense,
      "health": self.health,
      "stamina": self.stamina,
      "stamina_regen": self.stamina_regen,
      "mana": self.mana,
      "mana_regen": self.mana_regen,
      "abilities": self.abilities
    }


Card = namedtuple("Card", ["owner", "original_id", 'id'])


def update_database():
  dex = HoloDex()

  values = []

  for i in range(10):
    data = dex.get_channels(org=ORGS.ALL, offset=i*100)
    values += data

  with open('./holodex.db', 'a') as a:
    json.dump(values, a, indent=1)


def read():
  with open("./holodex.db", 'r') as r:
    data = json.load(r)
  return data

def get_randoms(count:int=1) -> list[Entry]:
  values = read().copy()
  out = []
  for i in range(count):
    value = choice(values)
    values.remove(value)
    out.append(value)
  return [Entry(**x) for x in out]
