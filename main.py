#!/usr/bin/env python2.7

"""
Platybot - An IRC bot,
Written by Samuel Leeuwenburg,
Used for experimentation with Python
"""

from connection import Connection
from bot import Bot

def main():

    conn = Connection()
    conn.connect()

    bot = Bot(conn)

    while True:
        bot.update_loop()
        log = conn.log()

        if log:
            bot.eat_log(log)
            print(log)


if __name__ == '__main__':
    main()
