class BoundingRect(object):
    def __init__(self, width, height):
        self.width = float(width)
        self.height = float(height)
        self.landscape = self.width >= self.height

    def set_size(self, width, height):
        use_height_for_ratio = (self.width - width) > (self.height - height)
        if use_height_for_ratio:
            self.crop_height = self.height
            self.crop_width = float(width) * float(self.height) / float(height)
        else:
            self.crop_width = self.width
            self.crop_height = float(height) * float(self.width) / float(width)

        self.top = ((float(self.height) - float(self.crop_height)) / 2) / float(self.height)
        if self.top < 0:
            self.top = 0.0
        self.bottom = 1.0 - self.top
        self.left = ((float(self.width) - float(self.crop_width)) / 2) / float(self.width)
        if self.left < 0:
            self.left = 0.0
        self.right = 1.0 - self.left

