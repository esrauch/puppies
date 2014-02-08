import webapp2
import jinja2
import json
import logging
import os
import random
import urllib
from google.appengine.api.urlfetch import fetch

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

BASE_PICASA_URL = 'https://picasaweb.google.com/data/feed/api/all?'

class MainPage(webapp2.RequestHandler):
  def get(self):
    # See https://developers.google.com/picasa-web/docs/2.0/developers_guide_protocol#ListCommunityPhotos
    picasa_url = BASE_PICASA_URL + urllib.urlencode({
      'tag': 'puppy',
      'max-results': 1,
      'alt': 'json',
      'start-index': random.randint(1, 100)
    })
    picasa_response_obj = fetch(picasa_url)
    picasa_response = json.loads(picasa_response_obj.content)
    first_entry = picasa_response['feed']['entry'][0]
    image_src = first_entry['content']['src']
    
    template_values = {
      'image_src': image_src
    }
    template = jinja_environment.get_template('index.html')
    self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)