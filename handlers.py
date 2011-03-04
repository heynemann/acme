#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import re
from os.path import join, splitext
from urlparse import urlparse

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api.images import Image, PNG, JPEG
from google.appengine.api import memcache

try:
  # When deployed
  from google.appengine.runtime import RequestTooLargeError
except ImportError:
  # In the development server
  from google.appengine.runtime.apiproxy_errors import RequestTooLargeError

from models import Picture, ImageNotFoundError, MAX_WIDTH, MAX_HEIGHT
from rect import BoundingRect
from settings import *

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

    def validate_url(self, url):
        if not url:
            self._error(400, 'The url argument is mandatory!')
            return

        url = join('http://', url)

        if not self._verify_allowed_domains():
            self._error(404, 'Your domain is not allowed!')
            return

        if not self._verify_allowed_sources(url):
            self._error(404, 'Your image source is not allowed!')
            return

        return url

    def transform(self, img, width, flip_horizontal, height, flip_vertical, image_format, halign="center", valign="middle"):
        if not width and not height:
            width = img.width
            height = img.height

        if float(width) / float(img.width) > float(height) / float(img.height):
            img.resize(width=width)
            image_width = width
            image_height = float(width) / float(img.width) * float(img.height)
        else:
            img.resize(height=height)
            image_width = float(height) / float(img.height) * float(img.width)
            image_height = height

        rect = BoundingRect(height=image_height, width=image_width)
        rect.set_size(height=height, width=width, halign=halign, valign=valign)

        if not width:
            width = rect.target_width
        if not height:
            height = rect.target_height

        img.crop(left_x=rect.left,
                 top_y=rect.top,
                 right_x=rect.right,
                 bottom_y=rect.bottom)

        if flip_horizontal:
            img.horizontal_flip()
        if flip_vertical:
            img.vertical_flip()

        return img.execute_transforms(output_encoding=image_format, quality=QUALITY)

    def get(self,
            flip_horizontal,
            width,
            flip_vertical,
            height,
            halign,
            valign,
            url):

        url = self.validate_url(url)

        width = width and int(width) or 0
        height = height and int(height) or 0

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

        extension = splitext(url)[-1]
        image_format = extension in ('.jpg', '.jpeg') and JPEG or PNG

        data = memcache.get(key)

        self.response.headers['Cache-Key'] = key
        if data is not None:
            results = data
            self.response.headers['Cache-Hit'] = 'True'
        else:
            query = "SELECT * FROM Picture WHERE url = :1 LIMIT 1"
            pictures = db.GqlQuery(query, url).fetch(1)

            try:
                if len(pictures) > 0: 
                    picture = pictures[0]
                    if picture.is_expired():
                        img = picture.fetch_image()
                        try:
                            picture.put()
                        except RequestTooLargeError:
                            picture.rebalance_picture_size(self.transform)
                            picture.put()
                    else:
                        img = Image(picture.picture)
                else:
                    picture = Picture()
                    picture.url = url
                    img = picture.fetch_image()
                    try:
                        picture.put()
                    except RequestTooLargeError:
                        picture.rebalance_picture_size(self.transform)
                        picture.put()
            except ImageNotFoundError:
                self._error(404, 'Your image source is not found!')
                return

            results = self.transform(img, width, flip_horizontal, height, flip_vertical, image_format, halign, valign)

            memcache.set(key=key,
                     value=results,
                     time=EXPIRATION) # ONE MONTH

            self.response.headers['Cache-Hit'] = 'False'

        self.response.headers['Content-Type'] = image_format == JPEG and 'image/jpeg' or 'image/png'
        self.response.out.write(results)

