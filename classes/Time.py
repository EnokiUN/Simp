from datetime import datetime

class Time:
  date_format_str = '%d/%m/%Y %H:%M:%S.%f'

  @classmethod
  def now(cls):
    return datetime.strftime(datetime.now(), cls.date_format_str)

  @classmethod
  def from_string(cls, string: str):
    return datetime.strptime(string, cls.date_format_str)

  @classmethod
  def get_hour_diff(cls, string1, string2):
    a = cls.from_string(string1)
    b = cls.from_string(string2)
    diff = a - b
    return abs(diff.total_seconds() / 3600)

  @classmethod
  def is_24_hours_ago(cls, string1):
    return cls.get_hour_diff(string1, cls.now()) >= 24.0
