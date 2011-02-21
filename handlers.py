#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import re
from os.path import join
from urlparse import urlparse

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api.images import Image, PNG
from google.appengine.api.urlfetch import Fetch
from google.appengine.api import memcache

from models import Picture
from rect import BoundingRect
from settings import ALLOWED_DOMAINS, ALLOWED_SOURCES

MAX_WIDTH = 1280
MAX_HEIGHT = 800

class MainHandler(webapp.RequestHandler):
    def _error(self, status, msg):
        self.error(status)
        self.response.out.write(msg)

    def _verify_allowed_domains(self):
        res = urlparse(self.request.url)
        for pattern in ALLOWED_DOMAINS:
            if re.match('^%s$' % pattern, res.hostname):
                return True
        return False

    def _verify_allowed_sources(self, url):
        res = urlparse(url)
        for pattern in ALLOWED_SOURCES:
            if re.match('^%s$' % pattern, res.hostname):
                return True
        return False

    def get(self,
            width,
            height,
            halign,
            valign,
            url):
        if not url:
            self._error(400, 'The url argument is mandatory!')
            return 

        if not width and not height:
            self._error(400, 'Either widht or height are mandatory!')

        url = join('http://', url)

        if not self._verify_allowed_domains():
            self._error(404, 'Your domain is not allowed!')
            return

        if not self._verify_allowed_sources(url):
            self._error(404, 'Your image source is not allowed!')
            return
 
        width = width and int(width) or None
        height = height and int(height) or None

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

            if (height / img.height) > (width / img.width):
                img.resize(height=height)
                image_width = float(height) / float(img.height) * float(img.width)
                image_height = height
            else:
                img.resize(width=width)
                image_width = width
                image_height = float(width) / float(img.width) * float(img.height)

            self.response.headers['width'] = image_width
            self.response.headers['height'] = image_height

            rect = BoundingRect(height=image_height, width=image_width)
            rect.set_size(height=height, width=width, halign=halign, valign=valign)

            img.crop(left_x=rect.left,
                     top_y=rect.top,
                     right_x=rect.right,
                     bottom_y=rect.bottom)

            results = img.execute_transforms(output_encoding=PNG, quality=95)

            #try:
            memcache.set(key=key,
                         value=results,
                         time=2) # ONE MONTH
            #except ValueError, err:
                #Ignore MemCache 1mb error
                #TODO: LOG ERROR
                #pass

            self.response.headers['Cache-Hit'] = 'False'

        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(results)

