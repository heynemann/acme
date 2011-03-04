#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import urllib2
from urllib2 import HTTPError
from os.path import splitext

from google.appengine.ext import db
from google.appengine.api.images import Image, PNG, JPEG

from settings import EXPIRATION_DB

MAX_WIDTH = 1280
MAX_HEIGHT = 800

class ImageNotFoundError(RuntimeError):
    pass

class Picture(db.Model):
    url = db.StringProperty()
    picture = db.BlobProperty(default=None)
    last_fetch = db.DateTimeProperty(auto_now=True)

    @property
    def extension(self):
        return splitext(self.url)[-1]

    @property
    def image_format(self):
        return self.extension in ('.jpg', '.jpeg') and JPEG or PNG

    def is_expired(self):
        expiration_time = self.last_fetch + datetime.timedelta(seconds=EXPIRATION_DB)
        return datetime.datetime.now() >= expiration_time

    def fetch_image(self):
        try:
            response = urllib2.urlopen(self.url)
        except HTTPError:
            raise ImageNotFoundError()
        contents = response.read()
        self.store_picture(contents)
        self.last_fetch = datetime.datetime.now()
        return Image(contents)

    def store_picture(self, picture):
        self.picture = db.Blob(picture)

    def rebalance_picture_size(self, resize_method):
        img = Image(self.picture)
        resize_width = img.width > img.height and MAX_WIDTH or 0
        resize_height = img.height >= img.width and MAX_HEIGHT or 0
        new_picture = resize_method(
            img,
            resize_width,
            '',
            resize_height,
            '',
            self.image_format,
            'center',
            'middle'
        )
        self.store_picture(new_picture)

