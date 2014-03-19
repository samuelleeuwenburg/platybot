import urllib2
import json

class MovieCommands:
  def __init__(self):
    self.name = 'tmdb'
    self.trigger = 'movie info '

    f = open('./config.json')
    self.config = json.loads(f.read())
    f.close()

    for keys in self.config['apiKeys']:
      if keys['name'] == self.name:
        self.apiKey = keys['key']

    self.url = 'https://api.themoviedb.org/3/'


  def handleCommand(self, conn, nick, chan, msg):

    cmd = msg.split(self.trigger)[1]

    if cmd.startswith('about'):
      self.search_movie(conn, nick, chan, msg)


  def search_movie(self, conn, nick, chan, msg):

    cmd = msg.split('about ')[1]

    response = urllib2.urlopen('http://api.themoviedb.org/3/search/movie?query=' + cmd.replace(' ', '%20') + '&api_key=' + self.apiKey)
    data = json.load(response)

    first_entry = data['results'][0]

    response = 'I found this for you %s: %s - release date: %s average rating: %s (from %s votes) - data by www.themoviedb.org' % (nick, first_entry['title'], first_entry['release_date'], first_entry['vote_average'], first_entry['vote_count'])

    conn.send_message(chan, response)
