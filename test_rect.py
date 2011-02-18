from rect import BoundingRect

def test_rect_for_landscape():
    rect = BoundingRect(width=640, height=480)
    rect.set_size(width=320, height=300)

    assert rect.crop_height == 480, rect.crop_height
    assert rect.crop_width == 512, rect.crop_width

def test_rect_for_landscape_using_width():
    rect = BoundingRect(width=640, height=480)
    rect.set_size(width=320, height=100)

    assert rect.crop_height == 200, rect.crop_height
    assert rect.crop_width == 640, rect.crop_width

def test_rect_for_landscape_even_when_changing_orientation():
    rect = BoundingRect(width=640, height=480)
    rect.set_size(width=300, height=340)

    assert rect.crop_height == 480, rect.crop_height
    assert rect.crop_width == 423, rect.crop_width

def test_rect_for_portrait():
    rect = BoundingRect(width=480, height=640)
    rect.set_size(width=300, height=320)

    assert rect.crop_height == 512, rect.crop_height
    assert rect.crop_width == 480, rect.crop_width

def test_rect_for_portrait_using_height():
    rect = BoundingRect(width=480, height=640)
    rect.set_size(width=100, height=320)

    assert rect.crop_height == 640, rect.crop_height
    assert rect.crop_width == 200, rect.crop_width

def test_rect_for_portrait_even_when_changing_orientation():
    rect = BoundingRect(width=480, height=640)
    rect.set_size(width=340, height=300)

    assert rect.crop_height == 423, rect.crop_height
    assert rect.crop_width == 480, rect.crop_width
