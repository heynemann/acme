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

from google.appengine.api import users
from google.appengine.api.images import Image, PNG
from google.appengine.api.urlfetch import Fetch
from google.appengine.api import memcache

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class MainHandler(webapp.RequestHandler):
    def get(self):
        url = "http://s.glbimg.com/jo/g1/f/original/2011/02/18/novaodessa__.jpeg"
        width = 300
        height = 214

        data = memcache.get(url)
        if data is not None:
            results = data
            self.response.headers['Cache-Hit'] = 'True'
        else:
            contents = Fetch(url).content
            img = Image(contents)

            rect = BoundingRect(img)
            rect.set_size(height, width)

            img.crop(
            img.resize(height=rect.resize_height, width=rect.resize_width)

            results = img.execute_transforms(output_encoding=PNG, quality=95)

            memcache.set(url, results, 1)

            self.response.headers['Cache-Hit'] = 'False'

        #im = get_thumbnail('http://s.glbimg.com/jo/g1/f/original/2011/02/18/novaodessa__.jpeg', '100x100', crop='center', quality=99)

        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(results)

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
