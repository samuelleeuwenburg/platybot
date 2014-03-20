import time
import json
import re
import random


class Communication:
  def __init__(self, conn):

    f = open('./settings.json')
    self.settings = json.loads(f.read())
    f.close()

    self.dictionary = self.settings['dictionary']
    self.nick = self.settings['nick']
    self.conn = conn

    self.reply_stack = []


  def reply_loop(self):
    ''' loop through the reply stack and determine if a message is ready to be send '''

    now = time.time()

    for reply in list(self.reply_stack):

      if reply['timestamp'] < now:
        self.conn.send_message(reply['channel'], reply['content'])
        self.reply_stack.remove(reply)


  def handle_message(self, nick, chan, msg):
    ''' Handle message and add (optional) response to the reply_stack '''


    for entry in self.dictionary:

      for match in entry['matches']:
        check = match.replace('{{self}}', self.nick)

        # remove all strange characters when checking with the dictionary
        if re.sub('[!?@#$,.]', '', msg) == check:

          response = entry['response'].replace('{{sender}}', nick)

          self.reply_stack.append({
            'content': response,
            'channel': chan,
            'timestamp': time.time() + random.randrange(3,7)
          })
