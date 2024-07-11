import unittest
import cv2
from image import Image


class TestImage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestImage, self).__init__(*args, **kwargs)
        self.cv2_object_1 = cv2.imread('test_images/alita01.jpg')
        self.cv2_object_2 = cv2.imread('test_images/batman01.png')

    def test_thresh_image(self):
        self.assertEqual(True, False)  # add assertion here

    def test_show_panel(self):
        self.assertEqual(True, False)

    def test_find_contours(self):
        self.assertEqual(True, False)

    def test_set_mask(self):
        image_1 = Image(self.cv2_object_1)
        image_1.set_mask(2)

        image_2 = Image(self.cv2_object_2)
        image_2.set_mask(400)

        self.assertEqual(image_1.get_mask(), 2)
        self.assertEqual(image_2.get_mask(), 400)

    def test_get_image(self):
        self.assertEqual(True, False)

    def test_corners(self):
        self.assertEqual(True, False)

    def test_index(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
