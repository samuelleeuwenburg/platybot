import re

class Bot:

  def __init__(self, conn, settings):
    self.conn = conn

    self.user = settings['user']
    self.nick = settings['nick']
    self.sudo_command = 'plat'

    self.channels = settings['channels']
    self.dictionary = settings['dictionary']

    conn.set_user(self.user)
    conn.set_nick(self.nick)

    for channel in self.channels:
      conn.join_channel(channel)


  def eat_log(self, log):
    """ Om nom nom nom, dem logs are tasty """

    if log.find(' PRIVMSG ') != -1:
      nick = log.split('!')[0][1:]
      chan = log.split(' PRIVMSG ')[-1].split(" :")[0]
      msg = log.split(' PRIVMSG ')[-1].split(':')[-1]

      # determine if the sudo command is being used, and act accordingly
      if msg.split(' ', 1)[0] == self.sudo_command:
        self.handle_command(nick, chan, msg.split(' ', 1)[0])
      else:
        self.handle_message(nick, chan, msg)


  def handle_message(self, nick, chan, msg):
    """ Handles regular message with responses out of the dictionary """

    for entry in self.dictionary:

      for match in entry['matches']:
        check = match.replace('{{self}}', self.nick)

        # remove all strange characters when checking with the dictionary
        if re.sub('[!@#$]', '', msg) == check:

          response = entry['response'].replace('{{sender}}', nick)
          self.conn.send_message(chan, response)

  def handle_command(self, nick, chan, msg):
    """ Handles commands, still in progress """

    response = nick + ': what?'
    self.conn.send_message(chan, response)
