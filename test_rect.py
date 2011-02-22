from rect import BoundingRect

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
