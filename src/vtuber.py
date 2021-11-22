
from typing import Any
import requests
import sqlite3
from collections import namedtuple
import json
from rich import print


Vtuber = namedtuple("Vtuber", [
    "id",
    "name",
    "english_name",
    "photo",
    "org",
    "suborg",
    "group",
    "lang",
    "published_at",
    "type",
    "youtube_id",
    "youtube_subs",
    "twitch_id",
    "twitch_follows",
    "twitter",
    "updated_at",
    "top_topics"
])


class Database:
    def __init__(self):
        self.con = sqlite3.connect("./vtubers.db")
        self.cur = self.con.cursor()
        self.vtuber_table = """
      vtubers(
      id INTEGER PRIMARY KEY,
      TEXT name,
      TEXT english_name,
      TEXT photo,
      TEXT org,
      TEXT suborg,
      TEXT group,
      TEXT lang,
      TEXT published_at,
      TEXT type,
      TEXT youtube_id,
      TEXT youtube_subs,
      TEXT twitch_id,
      TEXT twitch_follows,
      TEXT twitter,
      TEXT updated_at,
      TEXT top_topics,
      TEXT links
    )
    """

        self.cur.execute(f"""
    CREATE TABLE {self.vtuber_table} IF NOT EXISTS
    """)
        self.con.commit()

    def add_vtuber(self, vtuber: Vtuber):
        self.cur.execute(
            f"INSERT INTO vtubers{Vtuber._fields} VALUES ({'%s,'*len(Vtuber._fields)})", tuple(vtuber))
        self.conn.commit()

    def search_vtuber_by_name(self, query: str, en: bool = False):
        self.cur.execute(f"""
    SELECT * FROM vtubers WHERE {'name' if not en else 'english_name'} LIKE '%{query}%'
    """)
        return self.cur.fetchall()

    def search_vtuber_by_org(self, query: str, sub_org: bool = False):
        self.cur.execute(f"""
    SELECT * FROM vtubers WHERE {'org' if not sub_org else 'suborg'} LIKE '%{query}%'
    """)
        return self.cur.fetchall()

    def search_vtuber_by_twitter(self, query: str):
        self.cur.execute(f"""
    SELECT * FROM vtubers WHERE twitter LIKE '%{query}%'
    """)
        return self.cur.fetchall()

    def remove_vtuber(self, name: str):
        self.cur.execute(f"DELETE FROM vtubers WHERE name = '{name}'")
        self.con.commit()

    def update_vtuber(self, id: int, property: str, value: Any):
        self.cur.execute(
            f"UPDATE vtubers SET {property} = %s WHERE id = %s", (value, id))
        self.con.commit()


class Generator:
    def __init__(self):
        pass

    def data_from_youtube(self, youtube_id: str):
        res = requests.get(f"https://holodex.net/api/v2/channels/{youtube_id}")
        data = res.json()
        return data


vtuber_data = [
  'id',
  'name',
  'english_name',
  'description',
  'photo',
  'thumbnail',
  'banner',
  'org', 'suborg',
  'lang',
  'published_at',
  'view_count',
  'video_count',
  'subscriber_count',
  'comments_crawled_at',
  'updated_at',
  'yt_uploads_id',
  'crawled_at',
  'type',
  'clip_count',
  'twitter',
  'inactive',
  'created_at',
  'top_topics'
]


gen = Generator()

data = gen.data_from_youtube("UCaTUFB2QKcLDxdP3RcX3eFw")
print(data.keys())
