from google.appengine.ext import db

class Picture(db.Model):
    url = db.StringProperty()
    picture = db.BlobProperty(default=None)

