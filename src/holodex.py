import requests
from urllib.parse import urlencode, quote
import json
from typing import Literal, Union
from rich import print


# Source: https://holodex.net/channel


class Channel:
  def __init__(self, **data):
    self.id: str = None
    self.name: str = None
    self.english_name: str = None
    self.description: str = None
    self.photo: str = None
    self.thumbnail: str = None
    self.banner: str = None
    self.org: str = None
    self.suborg: str = None
    self.lang: str = None
    self.published_at: str = None
    self.video_count: str = None
    self.subscriber_count: str = None
    self.comments_crawled_at: str = None
    self.updated_at: str = None
    self.yt_uploads_id: str = None
    self.crawled_at: str = None
    self.type: str = None
    self.clip_count: int = None
    self.twitter: str = None
    self.inactive = False
    self.created_at: str = None
    self.top_topics: list[str] = []

    for key in data.keys():
      setattr(self, key, data[key])

  def __repr__(self) -> str:
    return f"Channel(id={self.id}, name={self.name}, org={self.org})"



class Entry:
  def __init__(self, **data):
    self.id = None
    self.name = None
    self.english_name: str = None
    self.type: str = None
    self.org: str = None
    self.group: str = None
    self.photo: str = None
    self.twitter: str = None
    self.video_count: str = None
    self.subscriber_count: str = None
    self.clip_count: str = None
    self.top_topics: list[str]

    for key in data.keys():
      setattr(self, key, data[key])

  def __repr__(self) -> str:
    return f"Entry(id={self.id}, name={self.name}, org={self.org})"


class ORGS:
  HOLOLIVE="Hololive"
  INDEPENDANT="Independant"
  ALL="All Vtubers"
  NIJISANJI="Nijisanji"


class HoloDex:
  def __init__(self):
    self.base = "https://holodex.net/api/v2/"

  def autocomplete_result(self, query: str):
    res = requests.get(f"{self.base}/search/autocomplete?{urlencode({'q':query})}")
    return res

  def get_video(self, id: str, lang="en", c=1):
    query = urlencode({"lang": lang, "c": c})
    url = f"{self.base}videos/{id}?{query}"

    res = requests.get(url)

    return res

  def get_channel_videos(self, channel_id: str, lang="en", type="stream%2Cplaceholder", include="clips%2Clive_info", limit=24, paginated=True):
    query = urlencode({
      "lang": lang,
      "type": type,
      "include": include,
      "limit": limit,
      "paginated": paginated
    })
    url = f"{self.base}channels/{channel_id}/videos?{query}"
    res = requests.get(url)
    return res

  def get_channel(self, id: str):
    res = requests.get(f"{self.base}channels/{id}")

    return res

  def get_channels(self, limit=100, offset=0, type="vtuber", org=ORGS.HOLOLIVE, sort="suborg", order="asc"):

    query = urlencode({
      "limit": limit,
      "offset": offset,
      "type": type,
      "org": org,
      "sort": sort,
      "order": order
    })

    res = requests.get(f"{self.base}channels?{query}")

    return res.json()
