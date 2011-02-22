#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import urllib2
from urllib2 import HTTPError

from google.appengine.ext import db
from google.appengine.api.images import Image

from settings import EXPIRATION_DB

class ImageNotFoundError(RuntimeError):
    pass

class Picture(db.Model):
    url = db.StringProperty()
    picture = db.BlobProperty(default=None)
    last_fetch = db.DateTimeProperty(auto_now=True)
    
    def is_expired(self):
        expiration_time = self.last_fetch + datetime.timedelta(seconds=EXPIRATION_DB)
        return datetime.datetime.now() >= expiration_time
        
    def fetch_image(self):
        try:
            response = urllib2.urlopen(self.url)
        except HTTPError:
            raise ImageNotFoundError()
        contents = response.read()
        self.picture = db.Blob(contents)
        self.last_fetch = datetime.datetime.now()
        return Image(contents)
            

