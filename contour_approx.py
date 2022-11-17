from PIL import Image as Img

# from tkinter import *
# from tkinter.ttk import *
from file_path import Folder
from logger import Info
import logger as log
import os

# import time
import cv2
import numpy as np

folder = Folder()
logger = log.initialize_log()

# START_TIME = float(time.time())
# FINAL_TIME = float(time.time()) - START_TIME
ASK_PANELS = True  # Set to true if you want to be prompted to check for new contours in the image.
ASK_SAVE = True  # Set to true if you want to be asked to save the current cropped image
SHOW_PANEL = True  # Set to true if you want to show the current cropped image


def image_save(crop_image, index):
    """
    Writes cropped image to the cropped directory.

    Creates the cropped directory if it does not exist
    and takes the name of the current file and adds the string "cropped_"
    in to the current file name to indicate it is a new image.
    It then takes the new name and new image and writes it to the cropped directory.

    Parameters
    ----------
    crop_image
    index

    Returns
    -------
    NONE
    """
    if not os.path.isdir(folder.CROPPED_DIR):
        os.mkdir(folder.CROPPED_DIR)
        log.write_info(Info.CREATE, folder, logger)

    file_name = os.path.basename(folder.IMAGE_NAME)
    folder.NEW_FILE_NAME = os.path.join(
        folder.CROPPED_DIR, "cropped_{}_".format(str(index)) + file_name
    )

    if ASK_SAVE:
        answer = input("Did you want to save this? Yes/no || Y/N\n").upper()
        if answer == "YES" or answer == "Y":
            if index == 0:
                folder.NEW_FILE_NAME = os.path.join(
                    folder.CROPPED_DIR, "cropped_0_" + file_name
                )
                cv2.imwrite(folder.NEW_FILE_NAME, crop_image)
                log.write_info(Info.SAVE, folder, logger)
            else:
                cv2.imwrite(folder.NEW_FILE_NAME, crop_image)
                log.write_info(Info.SAVE, folder, logger)
    else:
        cv2.imwrite(folder.NEW_FILE_NAME, crop_image)
        log.write_info(Info.SAVE, folder, logger)


# TODO look into having ask_panels creating all of the cropped images and then displaying those from an array or whatever
# that would store all of the images. Maybe a hidden directory that holds the images?
def initialize_image():
    """
    Grabs files in the images directory and processes them.

    Takes each file, grabs the name of the image, and then reads
    and sends the image to the function 'thresh_image' for processing.

    Returns
    -------
    NONE
    """
    log.write_info(Info.ACCESS, folder, logger)
    for file in folder.IMAGE_LIST:
        folder.NEW_MASK = 0
        folder.IMAGE_NAME = os.path.join(folder.IMAGE_DIR, file)
        image = cv2.imread(folder.IMAGE_NAME)
        print(file)
        thresh_image(image, 0, 0)

    log.write_info(Info.EXECUTE, folder, logger)
    # IMAGE_NAME = os.path.join(IMAGE_DIR, r"spiderman.jpeg")
    # image = cv2.imread(IMAGE_NAME)
    # thresh_image(image, 0, 0)


def thresh_image(image, i, index):
    """
    Takes an image and places image through threshold process

    The image parameter is converted to grayscale
    and then converted into a new image with threshold.
    With threshold, we assign pixel values with the given
    threshold values and then send that new threshold image
    to the function 'find_contour'

    Parameters
    ----------
    image
    i
    index

    Returns
    -------
    NONE
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 155, 255, i)
    cv2.imshow("thresh", thresh)
    cv2.waitKey(0)
    find_contour(image, thresh, index)


def check_next(image, new_mask, index):
    thresh_image(image, new_mask, index + 1)


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


def find_contour(image, thresh, index):
    """
    Finds the contours of the image.

    Determines whether the contour's highest and lowest coordinate
    are within a difference of 5 points. If they are within the
    difference of 5 points, it resends the image and applies a
    new mask through the function 'thresh_image' to try
    again and crop to a smaller image.

    This allows for the program to try and create a more accurate
    and smaller cropped image. If the image doesn't produce smaller
    coordinates, it then saves the image's original state.

    Parameters
    ----------
    image
    thresh
    index

    Returns
    -------
    NONE
    """
    # TODO
    # Figure out how to get rid of redundant cropped images when it shows more panels
    # Figure how to grab the contours of 'sorted_contours[index + 1]' and compare that to the current sorted_contours
    # could look at grabbing a second set of max and min with the index + 1 sorted_contours variable

    contours, hierarchy = cv2.findContours(
        thresh.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    try:
        c = sorted_contours[
            index
        ]  # changing the index changes the contour position that it crops
    except IndexError:
        log.write_info(Info.INDEX, folder, logger)
        return

    output = image.copy()
    cv2.drawContours(output, [c], -1, (0, 255, 0), 10)

    # future_pic = check_next(image, new_mask, index)  # have this save the variable so its as its own instance

    for eps in np.linspace(0.001, 0.05, 10):
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, eps * perimeter, True)
        output = image.copy()
        cv2.drawContours(output, [approx], -1, (0, 0, 255), 3)
        if eps == 0.05:
            dataY = []
            dataX = []
            np.array(dataX)
            np.array(dataY)

            for i in approx:
                for x, y in i:
                    dataX = np.append(dataX, x)
                    dataY = np.append(dataY, y)
            maxY = np.max(dataY)  # these are the lowest and highest points of the image
            minY = np.min(dataY)

            maxX = np.max(dataX)
            minX = np.min(dataX)

            print("number of corners", len(approx))
            # This is to safeguard against the cropped image just barely cropping just a couple
            # of coordinates. It resends it to try another threshold type

            if (
                int(image.shape[0]) - 5 <= int(maxY) <= int(image.shape[0])
                and folder.NEW_MASK < 4
            ):
                folder.NEW_MASK = folder.NEW_MASK + 1
                thresh_image(image, folder.NEW_MASK, index)

            elif maxX - 10 < minX or maxY - 10 < minY:
                folder.NEW_MASK += 1
                thresh_image(image, folder.NEW_MASK, index)

            elif maxX == minX or maxY == minY:
                index += 1
                thresh_image(image, folder.NEW_MASK, index)

            # Otherwise, crop the image with the highest and lowest coordinates the image provides
            # whether the threshold type counter (new_mask) runs out, or if a valid crop image is found
            else:
                # This if statement determines whether there were less than 4 points it then
                # crops the image from the minX variable all the way to image.shape[1] to
                # better approximate the panel it was trying to grab. Otherwise, it just crops
                # to the 4> point contour approximation which is most likely not the entirety of
                # the panel we want
                if len(approx) < 4:
                    crop_image = image[
                        int(minY) : int(maxY), int(minX) : int(image.shape[1])
                    ]
                    if SHOW_PANEL:
                        color_converted = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
                        show_panel(color_converted)
                    image_save(crop_image, index)
                    log.write_info(Info.RESENT, folder, logger)

                    if ASK_PANELS and index < 13:
                        new_panel(image, index)
                else:
                    crop_image = image[int(minY) : int(maxY), int(minX) : int(maxX)]
                    if SHOW_PANEL:
                        color_converted = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
                        show_panel(color_converted)
                    image_save(crop_image, index)
                    log.write_info(Info.RESENT, folder, logger)
                    if ASK_PANELS and index < 13:
                        new_panel(image, index)


def new_panel(image, index):
    ## TODO look at creating all the images and just indexing through the images that were created
    # might have to make find_contour a function that returns the cropped image
    answer = input("Would you like to check for more panels\n").upper()
    if answer == "YES" or answer == "Y":
        threshold_type = 0
        if index < 13:
            thresh_image(image, threshold_type, index + 1)


def main():
    # gui_panel()
    # create_collage()
    initialize_image()
    # log.write_info(Info.CREATE, folder, logger)


if __name__ == "__main__":
    main()
