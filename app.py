from flask import Flask
from threading import Thread

app = Flask("App")

@app.route('/')
def home():
  return "Hello Peko"

def run():
  app.run(
    host="0.0.0.0",
    port=3000,
    debug=True
  )

def keep_alive(with_join=False):
  t = Thread(target=run)
  t.start()
  if with_join is True:
    t.join()
