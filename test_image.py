import unittest
import cv2
from unittest import mock
from PIL import Image as Img
from image import Image


class TestImage(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestImage, self).__init__(*args, **kwargs)
        self.cv2_object_1 = cv2.imread('test_images/alita01.jpg')
        self.cv2_object_2 = cv2.imread('test_images/batman01.png')
        self.image_1 = Image(self.cv2_object_1)
        self.image_2 = Image(self.cv2_object_2)

    def test_thresh_image(self):
        self.image_1.thresh_image()
        self.assertIs(self.image_1.thresh, self.image_1.get_thresh())  # add assertion here

# TODO: Fix this test
    @mock.patch('image.Img')
    def test_show_panel(self, mock_image):
        test_cv = cv2.imread('test_images/alita01.jpg')
        test_image = Image(test_cv)
        test_image.show_panel()
        mock_image.Img.show_panel.assert_called_once()

    def test_find_contours(self):
        self.assertEqual(True, False)

    def test_set_mask(self):
        self.image_1.set_mask(2)
        self.image_2.set_mask(400)

        self.assertEqual(self.image_1.get_mask(), 2)
        self.assertEqual(self.image_2.get_mask(), 400)

    def test_get_image(self):
        self.assertIs(self.image_1.get_image(), self.cv2_object_1)
        self.assertIs(self.image_2.get_image(), self.cv2_object_2)

    def test_corners(self):
        self.image_1.thresh_image()
        self.image_1.find_contours()
        self.assertEqual(self.image_1.get_corners(), 2)

    def test_index(self):
        self.image_1.set_index(2)
        self.assertEqual(self.image_1.get_index(), 2)

        self.image_1.set_index(self.image_1.get_index() + 1)
        self.assertEqual(self.image_1.get_index(), 3)


if __name__ == '__main__':
    unittest.main()
