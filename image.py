from PIL import Image as Img
import cv2
import numpy as np


# TODO LOOK INTO SUPERS AND SUBCLASSES FOR THE IMAGES AND CROPPED IMAGES TO SEPARATE FURTHER
#  IMAGE WOULD BE THE SUPER AND THE SUBCLASS WOULD BE THE CROPPED IMAGE
class Image:
    def __init__(self, name, image):
        self.ret = None
        self.thresh = None
        self.approx = None
        self.cropped_images = []
        self.image = image
        self.name = name
        self.index = 0
        self.mask = 0
        self.max_y = 0
        self.min_y = 0
        self.max_x = 0
        self.min_x = 0

    def thresh_image(self):
        """
        Takes an image and places image through threshold process
        and then converted into a new image with threshold.
        With threshold, we assign pixel values with the given
        threshold values and then send that new threshold image
        to the function 'find_contours'
        Parameters
        ----------
        self
        Returns
        -------
        NONE
        """
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.ret, self.thresh = cv2.threshold(gray, 155, 255, self.mask)

        # TODO SHOW PANEL SHOULD BE USED TO SHOW THE DIFFERENT CROPPED AND REGULAR IMAGE PICTURES

    def show_panel(self):
        """
        Displays the current cropped_old image

        When this is called it takes a cropped_old image
        and displays it in separate window
        Parameters
        ----------
        self

        Returns
        -------
        NONE
        """
        pil_image = Img.fromarray(self.image)
        pil_image.show()

    def find_contours(self):
        contours, hierarchy = cv2.findContours(self.thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        try:
            c = sorted_contours[self.index]
        except IndexError:
            # Write logger: log.write_info(Info.INDEX, folder, logger)
            return
        output = self.image.copy()
        cv2.drawContours(output, [c], -1, (0, 255, 0), 10)

        for eps in np.linspace(0.001, 0.05, 10):
            perimeter = cv2.arcLength(c, True)
            self.approx = cv2.approxPolyDP(c, eps * perimeter, True)
            output = self.image.copy()
            cv2.drawContours(output, [self.approx], -1, (0, 0, 255), 3)
            if eps == 0.05:
                data_y = []
                data_x = []
                np.array(data_x)
                np.array(data_y)

                for i in self.approx:
                    for x, y in i:
                        data_x = np.append(data_x, x)
                        data_y = np.append(data_y, y)
                self.max_y = np.max(data_y)  # these are the lowest and highest points of the image
                self.min_y = np.min(data_y)
                self.max_x = np.max(data_x)
                self.min_x = np.min(data_x)

    def add_cropped_list(self, cropped_list):
        for image in cropped_list:
            self.cropped_images.append(image)

    def get_cropped_list(self):
        return self.cropped_images

    def next_panel(self):
        self.set_mask(0)
        self.set_index(self.get_index() + 1)

    def set_mask(self, mask):
        self.mask = mask

    def get_mask(self):
        return self.mask

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_corners(self):
        return len(self.approx)

    def get_max_y(self):
        return int(self.max_y)

    def get_min_y(self):
        return int(self.min_y)

    def get_max_x(self):
        return int(self.max_x)

    def get_min_x(self):
        return int(self.min_x)

    def get_shape(self, i):
        return int(self.image.shape[i])

    def set_index(self, index):
        self.index = index

    def get_index(self):
        return self.index

    def get_thresh(self):
        return self.thresh

    def get_name(self):
        return self.name
