from webtest import TestApp, AppError
from main import application

app = TestApp(application())

def test_request_valid_image():
    try:
        response = app.get("/200x100/right/middle/www.globo.com/media/globocom/img/sprite1.png")
    except AppError, e:
        assert False, "It need to be allowed."

def test_resquested_image_source_is_not_allowed():
    try:
        response = app.get("/200x100/right/middle/a2.twimg.com/a/1298499522/phoenix/img/twitter_logo_right.png")
        assert False, "It need to be not allowed."
    except AppError, e:
        assert str(e).endswith("Your image source is not allowed!")

    

