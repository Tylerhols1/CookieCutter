from PIL import Image
from tkinter import *
from tkinter.ttk import *
import os
import time
import cv2
import numpy as np
import logging

logging.basicConfig(filename="info.log", filemode="w", level=logging.INFO)
logger = logging.getLogger()

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGE_DIR = os.path.join(CURRENT_DIR, "images")
IMAGE_LIST = os.listdir(IMAGE_DIR)
CROPPED_DIR = os.path.join(CURRENT_DIR, "cropped")
IMAGE_NAME = ""
START_TIME = float(time.time())
FINAL_TIME = float(time.time()) - START_TIME
new_mask = 0

ASK_PANELS = True  # Set to true if you want to be prompted to check for new contours in the image.
ASK_SAVE = True  # Set to true if you want to be asked to save the current cropped image
SHOW_PANEL = True  # Set to true if you want to show the current cropped image


def create_collage():
    """

    Returns
    -------
    NONE
    """
    img1 = Image.open(r"images/guts_02.jpeg").convert('RGB')
    img2 = Image.open(r"images/berserkPanel.jpeg")
    x, y = img1.size
    print(img1.mode, img2.mode)
    img1.paste(img2, (0, 0))
    img1.show()


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
    if not os.path.isdir(CROPPED_DIR):
        os.mkdir(CROPPED_DIR)
        logger.info("CREATED CROPPED_DIR")

    file_name = os.path.basename(IMAGE_NAME)
    new_name = os.path.join(CROPPED_DIR, "cropped_{}_".format(str(index)) + file_name)

    if ASK_SAVE:
        answer = input("Did you want to save this? Yes/no || Y/N\n").upper()
        if answer == "YES" or answer == "Y":
            if index == 0:
                new_name = os.path.join(CROPPED_DIR, "cropped_0_" + file_name)
                cv2.imwrite(new_name, crop_image)
                logger.info("SAVED {}".format(os.path.basename(new_name)))
            else:
                cv2.imwrite(new_name, crop_image)
                logger.info("SAVED {}".format(os.path.basename(new_name)))
    else:
        cv2.imwrite(new_name, crop_image)
        logger.info("SAVED {}".format(os.path.basename(new_name)))


def initialize_image():
    """
    Grabs files in the images directory and processes them.

    Takes each file, grabs the name of the image, and then reads
    and sends the image to the function 'thresh_image' for processing.

    Returns
    -------
    NONE
    """
    global IMAGE_NAME
    global new_mask
    logger.info("ACCESSING {} file(s)\n".format(len(IMAGE_LIST)))
    for file in IMAGE_LIST:
        new_mask = 0
        IMAGE_NAME = os.path.join(IMAGE_DIR, file)
        image = cv2.imread(IMAGE_NAME)
        print(file)
        thresh_image(image, 0, 0)
    logger.info("PROGRAM EXECUTED IN {}".format(FINAL_TIME))
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
    find_contour(image, thresh, index)


def gui_panel():
    # TODO look into tkinter
    # add images to buttons in tkinter
    window = Tk()
    Label(window, text="window", font=("Courier New", 15)).pack(side=TOP, pady=10)
    photo = PhotoImage(file=r"images/batman01.png")
    photoimage = photo.subsample(2, 2)
    Button(window, image=photoimage, compound=LEFT).pack(side=BOTTOM, pady=10)
    mainloop()


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
    pil_image = Image.fromarray(image)
    pil_image.show()
    # cv2.imshow("crop", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


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
    global new_mask
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    try:
        c = sorted_contours[index]  # changing the index changes the contour position that it crops
    except IndexError:
        logger.error("WENT OUT OF INDEX, INDEXING IS OUT OF {} TIME(S)".format(len(sorted_contours)))
        return

    # c = max(contours, key=cv2.contourArea)

    output = image.copy()
    cv2.drawContours(output, [c], -1, (0, 255, 0), 10)

    for eps in np.linspace(0.001, 0.05, 10):
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, eps * perimeter, True)
        output = image.copy()
        cv2.drawContours(output, [approx], -1, (0, 0, 255), 3)
        if eps == .05:  # could look at changing this to check for the number of points
            dataY = []
            dataX = []
            # new dataX
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

            # This is to safeguard against the cropped image just barely cropping just a couple
            # of coordinates. It resends it to try another threshold type
            if int(image.shape[0]) - 5 <= int(maxY) <= int(image.shape[0]) and new_mask < 4:
                new_mask = new_mask + 1
                thresh_image(image, new_mask, index)

            elif maxX - 10 < minX or maxY - 10 < minY:
                new_mask += 1
                thresh_image(image, new_mask, index)

            elif maxX == minX or maxY == minY:
                index += 1
                thresh_image(image, new_mask, index)

            # Otherwise, crop the image with the highest and lowest coordinates the image provides
            # whether the threshold type counter (new_mask) runs out, or if a valid crop image is found
            else:
                # This if statement determines whether there were less than 4 points it then
                # crops the image from the minX variable all the way to image.shape[1] to
                # better approximate the panel it was trying to grab. Otherwise, it just crops
                # to the 4> point contour approximation which is most likely not the entirety of
                # the panel we want
                if len(approx) < 4:
                    crop_image = image[int(minY): int(maxY), int(minX): int(image.shape[1])]
                    if SHOW_PANEL:
                        show_panel(crop_image)
                    image_save(crop_image, index)
                    logger.info(
                        "RESENT {} THROUGH THRESHOLD {} TIME(S)\n".format(os.path.basename(IMAGE_NAME), new_mask))
                    if ASK_PANELS and index < 13:
                        new_panel(image, index)
                else:
                    crop_image = image[int(minY): int(maxY), int(minX): int(maxX)]
                    if SHOW_PANEL:
                        show_panel(crop_image)
                    image_save(crop_image, index)
                    logger.info(
                        "RESENT {} THROUGH THRESHOLD {} TIME(S)\n".format(os.path.basename(IMAGE_NAME), new_mask))
                    if ASK_PANELS and index < 13:
                        new_panel(image, index)


def new_panel(image, index):
    answer = input("Would you like to check for more panels\n").upper()
    if answer == "YES" or answer == "Y":
        threshold_type = 0
        if index < 13:
            thresh_image(image, threshold_type, index + 1)


def main():
    gui_panel()
    # create_collage()
    # initialize_image()


if __name__ == '__main__':
    main()
