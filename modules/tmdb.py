from urllib import quote
from urllib2 import HTTPError

import urllib2
import json
import random


class MovieCommands:
    def __init__(self):
        self.name = 'tmdb'
        self.command = 'movie '

        f = open('./config.json')
        self.config = json.loads(f.read())
        f.close()

        for keys in self.config['apiKeys']:
            if keys['name'] == self.name:
                self.apiKey = keys['key']

        self.url = 'https://api.themoviedb.org/3/'


    def post_movie_info(self, conn, nick, chan, movie):

        response = []
        response.append(movie['title'])
        response.append('Release date: %s' % (movie['release_date']))
        response.append('Average rating: %s (from %s votes)'% (movie['vote_average'], movie['vote_count']))
        response.append('Data by the www.themoviedb.org API')

        for line in response:
            conn.send_message(chan, line)


    def get_json_data(self, conn, chan, nick, params):
        try:
            response = urllib2.urlopen('http://api.themoviedb.org/3/' + params + '&api_key=' + self.apiKey)
        except urllib2.HTTPError, e:
            conn.send_message(chan, 'The API isn\'t responding, sorry ' + nick)
            return

        return response



    def handle_command(self, conn, nick, chan, msg):

        cmd = msg.split(self.command)[1]

        if cmd.startswith('search'):
            self.search_movie(conn, nick, chan, msg)
        elif cmd.startswith('from'):
            self.get_movie_from_year(conn, nick, chan, msg)




    def search_movie(self, conn, nick, chan, msg):

        if len(msg.split('search ')) == 1:
            conn.send_message(chan, 'Search for what ' + nick + '?')
            return

        cmd = msg.split('search ')[1].strip()

        response = self.get_json_data(conn, chan, nick, 'search/movie?query=' + quote(cmd))
        if not response:
            return

        data = json.load(response)

        if data['total_results'] == 0:
            conn.send_message(chan, 'Couldn\'t find anything ' + nick)
            return

        self.post_movie_info(conn, nick, chan, data['results'][0])




    def get_movie_from_year(self, conn, nick, chan, msg):
        if len(msg.split('from ')) == 1:
            conn.send_message(chan, 'From what year ' + nick + '?')
            return

        cmd = msg.split('from ')[1].strip()

        response = self.get_json_data(conn, chan, nick, 'discover/movie?year=' + quote(cmd))
        if not response:
            return

        data = json.load(response)

        if data['total_results'] == 0:
            conn.send_message(chan, 'Couldn\'t find anything ' + nick)
            return

        # If there are less then 2 pages, display the result. else query a random page
        if data['total_pages'] < 2:
            self.post_movie_info(conn, nick, chan, random.choice(data['results']))
            return

        # generate random page number
        number_of_pages = data['total_pages']
        target_page = random.randrange(1,number_of_pages)

        response = self.get_json_data(conn, chan, nick, 'discover/movie?year=' + quote(cmd) + '&page=' + str(target_page))
        if not response:
            return

        data = json.load(response)

        if data['total_results'] == 0:
            conn.send_message(chan, 'Couldn\'t find anything ' + nick)
            return

        self.post_movie_info(conn, nick, chan, random.choice(data['results']))
