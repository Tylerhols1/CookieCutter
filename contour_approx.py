from PIL import Image
import imutils
import os
import cv2
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
IMAGE_DIR = os.path.join(CURRENT_DIR, "images")
IMAGE_LIST = os.listdir(IMAGE_DIR)
CROPPED_DIR = os.path.join(CURRENT_DIR, "cropped")
IMAGE_NAME = ""
new_mask = 0
ASK_PANELS = True


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


def image_save(crop_image):
    """
    Writes cropped image to the cropped directory.

    Creates the cropped directory if it does not exist
    and takes the name of the current file and adds the string "cropped_"
    in to the current file name to indicate it is a new image.
    It then takes the new name and new image and writes it to the cropped directory.

    Parameters
    ----------
    crop_image

    Returns
    -------
    NONE
    """
    if not os.path.isdir(CROPPED_DIR):
        os.mkdir(CROPPED_DIR)

    file_name = os.path.basename(IMAGE_NAME)
    new_name = os.path.join(CROPPED_DIR, "cropped_" + file_name)
    cv2.imwrite(new_name, crop_image)
    # TODO
    'figure out how to log information of whether it saved or not'
    'could also write so it tracks how many times it had to apply'
    'new threshold type'


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
    for file in IMAGE_LIST:
        new_mask = 0
        IMAGE_NAME = os.path.join(IMAGE_DIR, file)
        image = cv2.imread(IMAGE_NAME)
        print(file)
        thresh_image(image, 0, 0)

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
    # cv2.imshow("thresh", thresh)
    # cv2.waitKey(0)
    find_contour(image, thresh, index)


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
    global new_mask
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    try:
        c = sorted_contours[index]  # changing the index changes the contour position that it crops
    except IndexError:
        c = sorted_contours[index + 1]

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
            print(dataX, "\n", dataY)
            maxY = np.max(dataY)  # these are the lowest and highest points of the image
            minY = np.min(dataY)

            maxX = np.max(dataX)
            minX = np.min(dataX)
            print(image.shape[0], image.shape[1])
            print("max and min for x", maxX, minX)
            print("max and min for Y", maxY, minY)

            # if int(maxY) < 0 or int(maxY) < int(minY):
            #    new_mask = new_mask + 1
            #    thresh_image(image, new_mask)

            # To safeguard against images not being approximated with smaller coordinates
            # than the overall image. It has it resend the image, so it is converted with
            # a new threshold type
            if int(image.shape[0]) - 5 <= int(maxY) <= int(image.shape[0]) and new_mask < 4:
                new_mask = new_mask + 1
                thresh_image(image, new_mask, index)
            # elif maxY == maxX
            # elif int(image.shape[1]) - 10 <= int(maxY) <= int(image.shape[1]) and new_mask < 4:
            #    new_mask = new_mask + 1  # look at randomizing this so that it checks different threshold types
            #    thresh_image(image, new_mask)

            # Otherwise, crop the image with the highest and lowest coordinates the image provides
            # whether the threshold type counter (new_mask) runs out, or if a valid crop image is found
            else:
                # This if statement determines whether there were less than 4 points it then
                # crops the image from the minX variable all the way to image.shape[1] to
                # better approximate the panel it was trying to grab. Otherwise, it just crops
                # to the 4> point contour approximation which is most likely not the entirety of
                # the panel we want

                # if there is an issue with an image not cropping correctly I could check to see how many points it has
                if len(approx) < 4:
                    crop_image = image[int(minY): int(maxY), int(minX): int(image.shape[1])]
                    cv2.imshow("crop", crop_image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    # image_save(crop_image)
                    if ASK_PANELS:
                        new_panel(image, index)

                else:
                    crop_image = image[int(minY): int(maxY), int(minX): int(maxX)]
                    cv2.imshow("crop", crop_image)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    # image_save(crop_image)
                    if ASK_PANELS:
                        new_panel(image, index)


def new_panel(image, index):
    answer = input("Would you like to check for more panels\n").upper()
    if answer == "YES":
        threshold_type = 0
        thresh_image(image, threshold_type, index + 1)


def main():
    # create_collage()
    initialize_image()


if __name__ == '__main__':
    main()
