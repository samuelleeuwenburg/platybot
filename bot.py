import json
import re

from modules import tmdb
from modules import communication
from modules import control

class Bot:

    def __init__(self, conn):
        f = open('config.json')
        self.config = json.loads(f.read())
        f.close()

        self.channels = self.config['channels']
        self.users_in_channel = {}

        self.conn = conn

        self.user = self.config['user']
        self.nick = self.config['nick']
        self.sudo_command = self.config['sudoCommand']
        self.mentors = self.config['mentors']

        conn.set_user(self.user)
        conn.set_nick(self.nick)

        for channel in self.channels:
            conn.join_channel(channel)
	
        self.communication = communication.Communication(self.conn, self.nick, self)

        # Add all commands into an array for easy checkups
        self.command_modules = []

        self.command_modules.append(tmdb.MovieCommands())
        self.command_modules.append(control.Control(self.conn, self.nick, self.mentors))


    def eat_log(self, log):
        """ Om nom nom nom, dem logs are tasty """

        if log.find(' PRIVMSG ') != -1:
            nick = log.split('!')[0][1:]
            chan = log.split(' PRIVMSG ')[-1].split(" :", 1)[0]
            msg = log.split(' PRIVMSG ')[-1].split(':', 1)[-1]

            # determine if the sudo command is being used, and act accordingly
            if msg.split(' ', 1)[0] == self.sudo_command:
                print chan + ': ' + msg

                self.handle_command(nick, chan, msg)
                return
            else:
                print chan + ': ' + msg

                self.handle_message(nick, chan, msg)
                return

        if log.find(' 353 ') != -1:
            self.update_rooms(log)
            return

        if log.find(' PART ') != -1:
            self.split_room(log)
            return 


    def update_rooms(self, log):
        # strip all prefix data before the equals sign
        if len(log.split('= ')) > 1:
            chan = log.split('= ')[1].split(' :')[0]
            users = re.sub('[@&~+%]', '', log.split('= ')[1].split(' :')[1].split('\r\n')[0]).split(' ')

            # set into users_in_channel dict
            self.users_in_channel[chan] = users

            print '$channels: ' + str(self.users_in_channel.keys())


    def split_room(self, log):
        chan = log.split(' PART ')[1]
       
        if chan in self.users_in_channel.keys():
            del self.users_in_channel[chan]

            print '$channels: ' + str(self.users_in_channel.keys())


    def update_loop(self):
        self.communication.response_loop()


    def handle_message(self, nick, chan, msg):
        """ Handles regular message by passing them to the communications module """
        self.communication.handle_message(nick, chan, msg)


    def handle_command(self, nick, chan, msg):
        """ Handles commands, based on all command modules registered """

        for module in self.command_modules:
            if msg.startswith(self.sudo_command + ' ' + module.command):
                module.handle_command(self.conn, nick, chan, msg)
                return

