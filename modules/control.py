import json

class Control:
    def __init__(self, conn, nick, mentors):

        self.name = 'control'
        self.command = 'do '

        self.conn = conn
        self.nick = nick
        self.mentors = mentors


    def handle_command(self, conn, nick, chan, msg):

        # check if the message is from a mentor
        if not nick in self.mentors:
            return False

        cmd = msg.split(self.command)[1]
        
        if cmd.startswith('join channel'):
            self.join_channel(conn, nick, chan, msg)
        elif cmd.startswith('leave channel'):
            self.leave_channel(conn, nick, chan, msg)


    def join_channel(self, conn, nick, chan, msg):

        channel = msg.split('join channel ')[1].strip()

        conn.join_channel(channel)

        response = 'Hello!'
        self.conn.send_message(channel, response)


    def leave_channel(self, conn, nick, chan, msg):

        channel = msg.split('leave channel ')[1].strip()

        response = 'bye bye!'
        self.conn.send_message(channel, response)

        conn.leave_channel(channel)
