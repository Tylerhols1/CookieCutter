from PIL import Image as Img
# from tkinter import *
# from tkinter.ttk import *
from file_path import Folder
from logger import Info
from image import Image
from cropped_image import Cropped
import logger as log
import os
import cv2

folder = Folder()
logger = log.initialize_log()
images = []
cropped_images = []


def create_cropped_dir():
    crop_dir = folder.get_cropped_path()
    if not os.path.isdir(crop_dir):
        os.mkdir(crop_dir)
        log.write_info(Info.CREATE, folder, logger, None)
    else:
        logger.info("THE DIRECTORY {} WAS ALREADY CREATED".format(folder.get_cropped_path()))


def initialize_images():
    """
    Grabs files in the images directory and processes them.

    Takes each file, grabs the name of the image, and then reads
    and sends the image to the function 'thresh_image' for processing.

    Returns
    -------
    NONE
    """
    log.write_info(Info.ACCESS, folder, logger, None)

    for file in folder.get_image_list():
        image_name = str(os.path.join(folder.get_image_dir_path(), file))
        cv2_object = cv2.imread(image_name)
        comic_image = Image(file, cv2_object)
        print("Name of the file: ", file)
        images.append(comic_image)


def initialize_cropped_images():
    global cropped_images
    image_list = []
    for image in images:
        index = 0
        while index < 13:
            image_shape = image.get_image()
            image_name = image.get_name()
            crop_image_name = str(
                os.path.join(folder.get_cropped_path(), "cropped_{}_{}".format(index, image.get_name())))

            # It is creating new objects which is why the images are not changing
            # Look at keeping track of the index and assigning it to a crop object instead
            # of the Image class keeping track of the index
            cropped_image = Cropped(image_shape, image_name, crop_image_name)

            check_corners(cropped_image)
            cv2.imwrite(crop_image_name, cropped_image.get_image())
            print(crop_image_name)
            image_list.append(cropped_image)
            cropped_image.next_panel()
            index += 1


def check_corners(comic_image):
    comic_image.thresh_image()
    comic_image.find_contours()

    min_x = comic_image.get_min_x()
    min_y = comic_image.get_min_y()
    max_x = comic_image.get_max_x()
    max_y = comic_image.get_max_y()
    image_mask = comic_image.get_mask()
    image_corners = comic_image.get_corners()
    image_index = comic_image.get_index()
    image = comic_image.get_image()

    if (comic_image.get_shape(0) - 5 <= max_y <= comic_image.get_shape(0) and image_mask < 4) or (
            max_x - 10 < min_x or max_y - 10 < min_y):
        comic_image.set_mask(comic_image.get_mask() + 1)
        check_corners(comic_image)

    elif max_x == min_x or max_y == min_y:
        comic_image.set_index(image_index + 1)
        check_corners(comic_image)
    # Otherwise, crop the image with the highest and lowest coordinates the image provides
    # whether the threshold type counter (new_mask) runs out, or if a valid crop image is found
    else:
        # This if statement determines whether there were less than 4 points it then
        # crops the image from the minX variable all the way to image.shape[1] to
        # better approximate the panel it was trying to grab. Otherwise, it just crops
        # to the 4> point contour approximation which is most likely not the entirety of
        # the panel we want
        if image_corners < 4:
            crop_image = image[min_y: max_y, min_x: image.shape[1]]
        else:
            crop_image = image[min_y: max_y, min_x: max_x]
        # cv2.imshow("crop_image", crop_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        comic_image.set_image(crop_image)
        # image_save(crop_image, image_index, comic_image)
        # log.write_info(Info.RESENT, folder, logger, comic_image)


def next_panel(comic_image):
    # TODO look at creating all the images and just indexing through the images that were created
    # might have to make find_contour a function that returns the cropped_old image
    # if ASK_PANELS:
    #    answer = input("Would you like to check for more panels\n").upper()
    #    if answer == "YES" or answer == "Y":
    comic_image.set_mask(0)
    comic_image.set_index(comic_image.get_index() + 1)


def main():
    create_cropped_dir()
    initialize_images()
    initialize_cropped_images()
    for i in cropped_images:
        print(i)
    # save_images()
    # TODO: Implement the global variables


if __name__ == "__main__":
    main()
