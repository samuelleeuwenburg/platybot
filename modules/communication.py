import time
import json
import re
import random


class Communication:
    def __init__(self, conn, nick, bot):

        f = open('./dictionary.json')
        self.dictionary = json.loads(f.read())
        f.close()

        self.replies = self.dictionary['replies']
        self.phrases = self.dictionary['phrases']
        self.nick = nick
        self.conn = conn
        self.bot = bot

        self.response_stack = []
        self.last_reply_per_channel = {}

        self.random_interval = 0
        self.reset_random_interval()
        

    def response_loop(self):
        ''' loop through the reply stack and determine if a message is ready to be send '''

        now = time.time()

        for response in list(self.response_stack):

            if response['timestamp'] < now:
                # respond
                self.conn.send_message(response['channel'], response['content'])

                print response['channel'] + ': ' + response['content']

                # remove from the stack
                self.response_stack.remove(response)

                # add to last messages dict
                self.last_reply_per_channel[response['channel']] = response['content']


        if self.random_interval < now:
            self.say_random_phrase()
            self.reset_random_interval()


    def reset_random_interval(self):

        floor = 400
        roof = 1200

        self.random_interval = time.time() + random.randrange(floor, roof);

    def handle_message(self, nick, chan, msg):
        ''' Handle message and add (optional) response to the reply_stack '''

        # check the message
        response = self.check_in_dictionary(msg)

        # then add it to the stack
        if not response:
            return

        # dice response
        if not self.dice_response(response):
            return

        self.add_to_stack(nick, chan, response['response'])


    def add_to_stack(self, nick, chan, response):

        # format the response for checkup
        formatted = self.format_response(response, nick)

        # if the response already exists return
        for response in list(self.response_stack):
            if response['content'] == formatted and response['channel'] == chan:
                return

        # if the response has just been said in the channel return
        try:
            self.last_reply_per_channel[chan]
        except:
            self.last_reply_per_channel[chan] = ''

        if self.last_reply_per_channel[chan] == formatted:
            return

        # add response to the stack
        self.response_stack.append({
            'content': formatted,
            'channel': chan,
            'timestamp': time.time() + random.randrange(3,7)
        })


    def format_response(self, response, nick):
        return response.replace('{{sender}}', nick)

    def format_phrase(self, phrase, room):
        response = phrase.replace('{{random nick}}', self.get_random_nick(room))
        response = response.replace('{{last nick}}', self.get_random_nick(room))

        return response
        
    def get_random_nick(self, room):
        # remove the bot from the name list
        if self.nick in self.bot.users_in_channel[room]:
            self.bot.users_in_channel[room].remove(self.nick)

        return random.choice(self.bot.users_in_channel[room])


    def get_last_nick(self, room):
        return 'not yet here'


    def dice_response(self, response):
        return 0 == random.randrange(0, response['odds'])


    def check_in_dictionary(self, msg):

        for entry in self.replies:

            for match in entry['matches']:

                # replace matched up string with our current nickname
                check = match.replace('{{self}}', self.nick)

                # remove all strange characters when checking with the replies
                if re.sub('[!?@#$,.]', '', msg).lower() == check.lower():

                    return entry

        return False


    def say_random_phrase(self):

        # check if we are in a room first.
        if len(self.bot.users_in_channel) > 0:
            room = random.choice(self.bot.users_in_channel.keys())
            phrase = self.format_phrase(random.choice(self.phrases)['phrase'], room)

            self.conn.send_message(room, phrase) 
        
