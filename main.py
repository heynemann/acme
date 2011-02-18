#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from os.path import join

from google.appengine.api import users
from google.appengine.api.images import Image, PNG
from google.appengine.api.urlfetch import Fetch
from google.appengine.api import memcache

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from rect import BoundingRect

class MainHandler(webapp.RequestHandler):
    def get(self, width, height, url):
        #url = "http://s.glbimg.com/jo/g1/f/original/2011/02/18/novaodessa__.jpeg"
        #width = 240
        #height = 100
        width = int(width)
        height = int(height)
        url = join('http://', url)

        data = memcache.get(url)
        if data is not None:
            results = data
            self.response.headers['Cache-Hit'] = 'True'
        else:
            contents = Fetch(url).content
            img = Image(contents)

            rect = BoundingRect(height=img.height, width=img.width)
            rect.set_size(height=height, width=width)

            self.response.headers['left-x'] = rect.left
            img.crop(left_x=rect.left,
                     top_y=rect.top,
                     right_x=rect.right,
                     bottom_y=rect.bottom)

            img.resize(height=height, width=width)

            results = img.execute_transforms(output_encoding=PNG, quality=95)

            memcache.set(url, results, 5)

            self.response.headers['Cache-Hit'] = 'False'

        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(results)

def main():
    application = webapp.WSGIApplication([('/(\d+)x(\d+)/(.+)', MainHandler)], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
