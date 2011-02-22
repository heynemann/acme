
import datetime

from google.appengine.api.images import Image

from models import Picture, ImageNotFoundError
from settings import EXPIRATION_DB

def test_lastfetch():
    picture = Picture()
    picture.last_fetch = datetime.datetime.now()
    assert picture.is_expired() == False

def test_lastfetch_expireted():
    picture = Picture()
    picture.last_fetch = datetime.datetime.now() - datetime.timedelta(seconds=EXPIRATION_DB + 1)
    assert picture.is_expired() == True
    
def test_fetchimage_latsfetch():
    old_fetch = datetime.datetime.now()
    picture = Picture()
    picture.url = "http://www.globo.com/media/globocom/img/sprite1.png"
    picture.fetch_image()
    assert picture.last_fetch > old_fetch
    
def test_fetchimage_return_image():
    picture = Picture()
    picture.url = "http://www.globo.com/media/globocom/img/sprite1.png"
    value_returned = picture.fetch_image()
    assert value_returned != None
    assert picture.picture != None
    
def test_fetchimage_notfound():
    picture = Picture()
    picture.url = "http://www.globo.com/media/globocom/noimage.png"
    try:
        picture.fetch_image()
        assert False
    except ImageNotFoundError:
        pass