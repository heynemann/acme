from rect import BoundingRect

def test_rect_for_landscape():
    rect = BoundingRect(width=640, height=480)
    rect.set_size(width=320, height=300)

    assert rect.crop_width == 640, rect.crop_width
    assert rect.crop_height == 450, rect.crop_height

def test_rect_percentages():
    rect = BoundingRect(width=640, height=480)
    rect.set_size(width=320, height=300)

    assert rect.left == 0.0, rect.left
    assert rect.right == 1.0, rect.right

    assert rect.top == 0.03125, rect.top
    assert rect.bottom == 0.96875, rect.bottom

def test_rect_percentages_portrait():
    rect = BoundingRect(width=480, height=640)
    rect.set_size(width=300, height=320)

    assert rect.left == 0.03125, rect.left
    assert rect.right == 0.96875, rect.right

    assert rect.top == 0.0, rect.top
    assert rect.bottom == 1.0, rect.bottom

def test_rect_for_landscape_using_width():
    rect = BoundingRect(width=640, height=480)
    rect.set_size(width=320, height=100)

    assert rect.crop_height == 150, rect.crop_height
    assert rect.crop_width == 640, rect.crop_width

def test_rect_for_landscape_even_when_changing_orientation():
    rect = BoundingRect(width=640, height=480)
    rect.set_size(width=300, height=340)

    assert rect.crop_height == 480, rect.crop_height
    assert int(rect.crop_width) == 564, rect.crop_width

def test_rect_for_portrait():
    rect = BoundingRect(width=480, height=640)
    rect.set_size(width=300, height=320)

    assert rect.crop_height == 640, rect.crop_height
    assert rect.crop_width == 450, rect.crop_width

def test_rect_for_portrait_using_height():
    rect = BoundingRect(width=480, height=640)
    rect.set_size(width=100, height=320)

    assert rect.crop_height == 640, rect.crop_height
    assert rect.crop_width == 150, rect.crop_width

def test_rect_for_portrait_even_when_changing_orientation():
    rect = BoundingRect(width=480, height=640)
    rect.set_size(width=340, height=300)

    assert int(rect.crop_height) == 564, rect.crop_height
    assert rect.crop_width == 480, rect.crop_width

def test_rect_weird_scenario():
    rect = BoundingRect(width=620, height=466)
    rect.set_size(width=100, height=50, valign="middle", halign="center")

    assert rect.crop_height == 233, rect.crop_height
    assert rect.crop_width == 620, rect.crop_width

def test_rect_weird_scenario_2():
    rect = BoundingRect(width=620, height=466)
    rect.set_size(width=50, height=100, valign="middle", halign="center")

    assert rect.crop_height == 466, rect.crop_height
    assert rect.crop_width == 310, rect.crop_width
