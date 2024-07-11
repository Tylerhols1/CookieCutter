from PIL import Image as Img
# from tkinter import *
# from tkinter.ttk import *
from file_path import Folder
from logger import Info
from image import Image
import logger as log
import os
import cv2

folder = Folder()
logger = log.initialize_log()
comic_images = []
# START_TIME = float(time.time())
# FINAL_TIME = float(time.time()) - START_TIME

ASK_PANELS = True  # Set to true if you want to be prompted to check for new contours in the image.
ASK_SAVE = False  # Set to true if you want to be asked to save the current cropped_old image
SHOW_PANEL = False  # Set to true if you want to show the current cropped_old image


def image_save(crop_image, index, comic_image):
    """
    Writes cropped_old image to the cropped_old directory.

    Creates the cropped_old directory if it does not exist
    and takes the name of the current file and adds the string "cropped_"
    in to the current file name to indicate it is a new image.
    It then takes the new name and new image and writes it to the cropped_old directory.

    Parameters
    ----------
    crop_image
    index
    comic_image

    Returns
    -------
    NONE
    """
    if not os.path.isdir(folder.CROPPED_DIR):
        os.mkdir(folder.CROPPED_DIR)
        log.write_info(Info.CREATE, folder, logger, comic_image)

    file_name = os.path.basename(folder.IMAGE_NAME)
    folder.NEW_FILE_NAME = os.path.join(
        folder.CROPPED_DIR, "cropped_{}_".format(str(index)) + file_name
    )
    print(str(folder.NEW_FILE_NAME))
    print("Crop: ", type(crop_image))
    if ASK_SAVE:
        answer = input("Did you want to save this? Yes/no || Y/N\n").upper()
        if answer == "YES" or answer == "Y":
            cv2.imwrite(str(folder.NEW_FILE_NAME), crop_image)
            log.write_info(Info.SAVE, folder, logger, comic_image)
    else:
        cv2.imwrite(str(folder.NEW_FILE_NAME), crop_image)
        log.write_info(Info.SAVE, folder, logger, comic_image)


# TODO look into having ask_panels creating all of the cropped_old images and then displaying those from an array or
#  whatever that would store all of the images. Maybe a hidden directory that holds the images?
def initialize_image():
    """
    Grabs files in the images directory and processes them.

    Takes each file, grabs the name of the image, and then reads
    and sends the image to the function 'thresh_image' for processing.

    Returns
    -------
    NONE
    """
    log.write_info(Info.ACCESS, folder, logger, None)

    # for file in folder.IMAGE_LIST:
    #    folder.IMAGE_NAME = os.path.join(folder.IMAGE_DIR, file)
    #    image = cv2.imread(folder.IMAGE_NAME)
    #    image_object = Image(image)
    #    print("Name of the file: ", file)
    #    new_thresh = thresh_object.thresh_image(thresh_object.image, 0, 0)
    #    find_contour(thresh_object.image, new_thresh, thresh_object.index)
    #    # # when this function does its thing there is no way to check and compare teh new thresh because it's not in
    #    # a loop

    for file in folder.IMAGE_LIST:
        folder.IMAGE_NAME = os.path.join(folder.IMAGE_DIR, file)
        cv2_object = cv2.imread(str(folder.IMAGE_NAME))
        comic_image = Image(cv2_object)
        comic_images.append(comic_image)
        print("Name of the file: ", file)
        comic_image.thresh_image()
        comic_image.find_contours()
        check_corners(comic_image)
        log.write_info(Info.EXECUTE, folder, logger, comic_image)


def check_corners(comic_image):
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
        # folder.NEW_MASK += 1
        # another_thresh = thresh_object.thresh_image(image, folder.NEW_MASK, index)
        # find_contour(thresh_object.image, another_thresh, thresh_object.index)
        comic_image.set_mask(comic_image.get_mask() + 1)
        comic_image.thresh_image()
        comic_image.find_contours()
        check_corners(comic_image)

    elif max_x == min_x or max_y == min_y:
        # index += 1
        # another_thresh = thresh_object.thresh_image(image, folder.NEW_MASK, index)
        # find_contour(thresh_object.image, another_thresh, thresh_object.index)
        comic_image.set_index(comic_image.get_index() + 1)
        comic_image.thresh_image()
        comic_image.find_contours()
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
            # crop_image = image[
            #              int(minY): int(maxY), int(minX): int(image.shape[1])
            #              ]
            crop_image = image[min_y: max_y, min_x: image.shape[1]]
            if SHOW_PANEL:
                # color_converted = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
                # show_panel(color_converted)
                show_panel(crop_image)

            image_save(crop_image, image_index, comic_image)
            log.write_info(Info.RESENT, folder, logger, comic_image)

            if ASK_PANELS and image_index < 13:
                new_panel(comic_image, image_index)
        else:
            crop_image = image[min_y: max_y, min_x: max_x]
            if SHOW_PANEL:
                color_converted = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
                show_panel(color_converted)
            image_save(crop_image, image_index, comic_image)
            log.write_info(Info.RESENT, folder, logger, comic_image)
            if ASK_PANELS and image_index < 13:
                new_panel(comic_image, image_index)


def show_panel(image):
    """
    Displays the current cropped image

    When this is called it takes a cropped image
    and displays it in separate window
    Parameters
    ----------
    image

    Returns
    -------
    NONE
    """
    pil_image = Img.fromarray(image)
    pil_image.show()


def new_panel(comic_image, index):
    ## TODO look at creating all the images and just indexing through the images that were created
    # might have to make find_contour a function that returns the cropped_old image
    answer = input("Would you like to check for more panels\n").upper()
    if answer == "YES" or answer == "Y":
        if index < 13:
            comic_image.set_mask(0)
            comic_image.set_index(comic_image.get_index() + 1)
            comic_image.thresh_image()
            comic_image.find_contours()
            check_corners(comic_image)


def main():
    # gui_panel()
    # create_collage()
    initialize_image()
    # log.write_info(Info.CREATE, folder, logger)
    # log.write_info(Info.SAVE, folder, logger)
    # log.write_info(Info.ACCESS, folder, logger)
    # log.write_info(Info.RESENT, folder, logger)


if __name__ == "__main__":
    main()
