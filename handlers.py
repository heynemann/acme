#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from os.path import join
from urlparse import urlparse

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api.images import Image, PNG
from google.appengine.api.urlfetch import Fetch
from google.appengine.api import memcache

from models import Picture
from rect import BoundingRect
from settings import ALLOWED_DOMAINS

MAX_WIDTH = 1280
MAX_HEIGHT = 800

class MainHandler(webapp.RequestHandler):
    def _error(self, status, msg):
        self.error(status)
        self.response.out.write(msg)
 
    def get(self,
            width,
            height,
            halign,
            valign,
            url):
        res = urlparse(self.request.url)

        if res.hostname not in ALLOWED_DOMAINS:
            self._error(404, 'Your domain is not allowed!')
            return

        if not url:
            self._error(400, 'The url argument is mandatory!')
            return 

        if not width and not height:
            self._error(400, 'Either widht or height are mandatory!')

        width = width and int(width) or None
        height = height and int(height) or None
        url = join('http://', url)

        if width > MAX_WIDTH:
            width = MAX_WIDTH
        if height > MAX_HEIGHT:
            height = MAX_HEIGHT

        if not halign:
            halign = "center"
        if not valign:
            valign = "middle"

        key = "%d_%d_%s_%s_%s" % (
                width,
                height,
                halign,
                valign,
                url
        )

        data = memcache.get(key)
        self.response.headers['Cache-Key'] = key
        if data is not None:
            results = data
            self.response.headers['Cache-Hit'] = 'True'
        else:
            query = "SELECT * FROM Picture WHERE url = :1 LIMIT 1"
            pictures = db.GqlQuery(query, url).fetch(1)

            if len(pictures) > 0:
                picture = pictures[0]
                img = Image(picture.picture)
            else:
                contents = Fetch(url).content
                img = Image(contents)
                picture = Picture()
                picture.url = url
                picture.picture = db.Blob(contents)
                picture.put()

            rect = BoundingRect(height=img.height, width=img.width)
            rect.set_size(height=height, width=width, halign=halign, valign=valign)

            img.crop(left_x=rect.left,
                     top_y=rect.top,
                     right_x=rect.right,
                     bottom_y=rect.bottom)

            img.resize(height=rect.target_height, width=rect.target_width)

            results = img.execute_transforms(output_encoding=PNG, quality=95)

            #try:
            memcache.set(key=key,
                         value=results,
                         time=15) # ONE MONTH
            #except ValueError, err:
                #Ignore MemCache 1mb error
                #TODO: LOG ERROR
                #pass

            self.response.headers['Cache-Hit'] = 'False'

        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(results)

