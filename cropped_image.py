from image import Image


class Cropped(Image):
    def __init__(self, image, orig_name, crop_name):
        super().__init__(orig_name, image)
        self.crop_name = crop_name
        self.crop_image = None

    def get_crop_name(self):
        return self.crop_name

    def set_crop_name(self, crop_name):
        self.crop_name = crop_name

    # def get_crop_image(self):
    #     return self.crop_image

    # def set_crop_image(self, crop_image):
    #     self.crop_image = crop_image
