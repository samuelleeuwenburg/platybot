import socket

class Connection:

  def __init__(self, settings):
    self.server = settings['server']
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def connect(self):
    self.conn.connect((self.server, 6667))

  def log(self):
    log = self.conn.recv(2048)
    log = log.strip('\n\r')

    # check to see if the server is pinging us
    if log.find('PING :') != -1:
      self.ping()
    else:
      return log

  def ping(self):
    self.conn.send('PONG :pingis\n')

  def send_message(self, chan, msg):
    self.conn.send('PRIVMSG ' + chan + ' :' + msg + '\n')

  def join_channel(self, chan):
    self.conn.send('JOIN '+ chan +'\n')

  def set_nick(self, nick):
    self.conn.send('USER '+ nick +' '+ nick +' '+ nick +' : Platypus as made by Samuel.\n')
    self.conn.send('NICK '+ nick +'\n')
