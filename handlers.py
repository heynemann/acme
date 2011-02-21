#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from os.path import join

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api.images import Image, PNG
from google.appengine.api.urlfetch import Fetch
from google.appengine.api import memcache

from models import Picture
from rect import BoundingRect

class MainHandler(webapp.RequestHandler):
    def get(self,
            width,
            height,
            halign,
            valign,
            url):
        if not url:
            self.error(400)

        if not width and not height:
            self.error(400)

        width = width and int(width) or None
        height = height and int(height) or None
        url = join('http://', url)

        if not halign:
            halign = "center"
        if not valign:
            valign = "middle"


        data = memcache.get(url)
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

            self.response.headers['left-x'] = rect.left
            img.crop(left_x=rect.left,
                     top_y=rect.top,
                     right_x=rect.right,
                     bottom_y=rect.bottom)

            img.resize(height=rect.target_height, width=rect.target_width)

            results = img.execute_transforms(output_encoding=PNG, quality=95)

            memcache.set(key=url,
                         value=results,
                         time=2592000) # ONE MONTH

            self.response.headers['Cache-Hit'] = 'False'

        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(results)

