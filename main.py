#!/usr/bin/python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from handlers import *
from settings import DEBUG

def application():
    webapp = webapp.WSGIApplication([
        ('/(-)?(\d+)?x(-)?(\d+)?/(?:(left|right|center)/)?(?:(top|bottom|middle)/)?/?(.+)', MainHandler)
    ], debug=DEBUG)
    return webapp

def main():
    util.run_wsgi_app(application())

if __name__ == '__main__':
    main()
