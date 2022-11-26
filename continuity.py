from threading import Thread
from flask import Flask

app = Flask("")


@app.route("/")
def run():
  app.run(host='0.0.0.0', port=8080)


def continuity():
  c = Thread(target=run)
  c.start()
