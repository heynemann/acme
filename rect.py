class BoundingRect(object):
    def __init__(self, width, height):
        self.width = float(width)
        self.height = float(height)
        self.landscape = self.width >= self.height

    def set_size(self, width, height, halign, valign):
        self.target_width = width
        self.target_height = height

        self.calculate_proportional_dimensions()

        use_height_for_ratio = (self.width - self.target_width) > (self.height - self.target_height)
        if use_height_for_ratio:
            self.crop_height = self.height
            self.crop_width = float(self.target_width) * float(self.height) / float(self.target_height)
        else:
            self.crop_width = self.width
            self.crop_height = float(self.target_height) * float(self.width) / float(self.target_width)

        self.calculate_crops(halign, valign)

    def calculate_proportional_dimensions(self):
        if not self.target_width:
            self.target_width = int(self.target_height * self.width / self.height)

        if not self.target_height:
            self.target_height = int(self.target_width * self.height / self.width)

    def calculate_crops(self, halign, valign):
        self.top = ((float(self.height) - float(self.crop_height)) / 2) / float(self.height)
        if self.top < 0:
            self.top = 0.0
        self.bottom = 1.0 - self.top

        if valign == "top":
            self.bottom = 1.0 - (2 * self.top)
            self.top = 0.0
        elif valign == "bottom":
            self.top = 2 * self.top
            self.bottom = 1.0

        self.left = ((float(self.width) - float(self.crop_width)) / 2) / float(self.width)
        if self.left < 0:
            self.left = 0.0
        self.right = 1.0 - self.left

        if halign == "left":
            self.right = 1.0 - (2 * self.left)
            self.left = 0.0
        elif halign == "right":
            self.left = 2 * self.left
            self.right = 1.0
