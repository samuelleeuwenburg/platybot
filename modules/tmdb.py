import urllib2
import json

class MovieCommands:
  def __init__(self):
    self.name = 'tmdb'
    self.command = 'movie'

    f = open('./config.json')
    self.config = json.loads(f.read())
    f.close()

    for keys in self.config['apiKeys']:
      if keys['name'] == self.name:
        self.apiKey = keys['key']

    self.url = 'https://api.themoviedb.org/3/'


  def handleCommand(self, conn, nick, chan, msg):

    cmd = msg.split(self.command)[1]

    if cmd.startswith('search'):
      self.search_movie(conn, nick, chan, msg)


  def search_movie(self, conn, nick, chan, msg):

    cmd = msg.split('search ')[1]

    response = urllib2.urlopen('http://api.themoviedb.org/3/search/movie?query=' + cmd.replace(' ', '%20') + '&api_key=' + self.apiKey)
    data = json.load(response)

    first_entry = data['results'][0]

    response = []
    response.append('I found this %s, ' % (nick))
    response.append(first_entry['title'])
    response.append('Release date: %s' % (first_entry['release_date']))
    response.append('Average rating: %s (from %s votes)'% (first_entry['vote_average'], first_entry['vote_count']))
    response.append('Data by www.themoviedb.org API')

    for line in response:
      conn.send_message(chan, line)
