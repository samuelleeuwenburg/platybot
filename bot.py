import re
import json

from modules import tmdb

class Bot:

  def __init__(self, conn):
    f = open('settings.json')
    self.settings = json.loads(f.read())
    f.close()

    f = open('config.json')
    self.config = json.loads(f.read())
    f.close()

    self.channels = self.config['channels']
    self.dictionary = self.settings['dictionary']

    self.conn = conn

    self.user = self.settings['user']
    self.nick = self.settings['nick']
    self.sudo_command = self.config['sudoCommand']

    conn.set_user(self.user)
    conn.set_nick(self.nick)

    for channel in self.channels:
      conn.join_channel(channel)

    # Add all commands into an array for easy checkups
    self.commandList = []

    self.commandList.append(tmdb.MovieCommands())


  def eat_log(self, log):
    """ Om nom nom nom, dem logs are tasty """

    if log.find(' PRIVMSG ') != -1:
      nick = log.split('!')[0][1:]
      chan = log.split(' PRIVMSG ')[-1].split(" :", 1)[0]
      msg = log.split(' PRIVMSG ')[-1].split(':', 1)[-1]

      # determine if the sudo command is being used, and act accordingly
      if msg.split(' ', 1)[0] == self.sudo_command:
        self.handle_command(nick, chan, msg)
      else:
        self.handle_message(nick, chan, msg)


  def handle_message(self, nick, chan, msg):
    """ Handles regular message with responses out of the dictionary """

    for entry in self.dictionary:

      for match in entry['matches']:
        check = match.replace('{{self}}', self.nick)

        # remove all strange characters when checking with the dictionary
        if re.sub('[!?@#$,.]', '', msg) == check:

          response = entry['response'].replace('{{sender}}', nick)
          self.conn.send_message(chan, response)

  def handle_command(self, nick, chan, msg):
    """ Handles commands, still in progress """

    for command in self.commandList:
      if msg.startswith(self.sudo_command + ' ' + command.trigger):
        command.handleCommand(self.conn, nick, chan, msg)
        return

    response = nick + ': what?'
    self.conn.send_message(chan, response)
