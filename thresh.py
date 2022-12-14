import cv2

class Thresh:
    def __init__(self, image):
        self.index = 0
        self.image = image
        self.mask = 0

def thresh_image(image, mask, index):
    """
    Takes an image and places image through threshold process
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
    Thresh.image = image
    Thresh.mask = mask
    Thresh.index = index

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 155, 255, mask)
    cv2.imshow("thresh", thresh)
    cv2.waitKey(0)
    return thresh
    #find_contour(image, thresh, index)