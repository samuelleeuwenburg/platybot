from connection import Connection
from bot import Bot
import json


def main():
  f = open('settings.json')
  settings = json.loads(f.read())
  f.close()

  conn = Connection(settings['connection'])
  conn.connect()

  bot = Bot(conn, settings['bot'])
  
  while True:
    log = conn.log()

    if log:
      bot.eat_log(log)
      print(log)


if __name__ == "__main__":
  main()
