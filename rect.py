class BoundingRect(object):
    def __init__(self, width, height):
        self.width = float(width)
        self.height = float(height)
        self.landscape = self.width >= self.height

    def set_size(self, width, height):
        use_height_for_ratio = (self.width - width) > (self.height - height)
        if use_height_for_ratio:
            self.crop_height = self.height
            self.crop_width = int(float(width) * float(self.height) / float(height))
        else:
            self.crop_width = self.width
            self.crop_height = int(float(height) * float(self.width) / float(width))
