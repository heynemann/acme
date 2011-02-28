from rect import BoundingRect

def test_rect_percentages():
    rect = BoundingRect(width=640, height=480)
    rect.set_size(width=320, height=300)

    assert rect.left == 0.25, rect.left
    assert rect.right == 0.75, rect.right

    assert rect.top == 0.1875, rect.top
    assert rect.bottom == 0.8125, rect.bottom

def test_rect_percentages_portrait():
    rect = BoundingRect(width=480, height=640)
    rect.set_size(width=300, height=320)

    assert rect.left == 0.1875, rect.left
    assert rect.right == 0.8125, rect.right

    assert rect.top == 0.25, rect.top
    assert rect.bottom == 0.75, rect.bottom
