from image import Image


class Cropped(Image):
    def __init__(self, image, orig_name, crop_name, index):
        super().__init__(orig_name, image)
        self.crop_name = crop_name
        self.crop_image = None
        self.index = index

    def get_crop_name(self):
        return self.crop_name

    def set_crop_name(self, crop_name):
        self.crop_name = crop_name

    def get_index(self):
        return self.index

    def set_index(self):
        self.index = index

    # def get_crop_image(self):
    #     return self.crop_image

    # def set_crop_image(self, crop_image):
    #     self.crop_image = crop_image
