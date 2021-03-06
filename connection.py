import socket
import json

class Connection:

    def __init__(self):
        f = open('config.json')
        self.config = json.loads(f.read())
        f.close()

        self.server = self.config['server']
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
	self.conn.connect((self.server, 6667))
        self.conn.settimeout(0.1)

    def log(self):

        try:
            log = self.conn.recv(2048)
        except socket.timeout, e:
            return
	
        log = log.decode('utf8', 'ignore')
        log = log.encode('ascii', 'ignore')
        log = log.strip('\n\r')

        # check to see if the server is pinging us, if so respond.
        if log.find('PING :') != -1:
            self.ping()
        else:
            return log

    def ping(self):
        self.conn.send('PONG :pingis\n')

    def send_message(self, chan, msg):
        msg = msg.encode('ascii', 'ignore')
        self.conn.send('PRIVMSG ' + chan + ' :' + msg + '\n')

    def get_users_in_channel(self, chan):
        self.conn.send('NAMES ' + chan + '\n')

    def join_channel(self, chan):
        self.conn.send('JOIN '+ chan +'\n')
        self.get_users_in_channel(chan)

    def leave_channel(self, chan):
        self.conn.send('PART '+ chan +'\n')

    def set_user(self, user):
        self.conn.send('USER '+ user)

    def set_nick(self, nick):
        self.conn.send('NICK '+ nick +'\n')
