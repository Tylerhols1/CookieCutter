from PIL import Image
import imutils
import cv2
import numpy as np

image = cv2.imread("/Users/tylerholstein/Documents/Fun Code/CookieCutter/square.jpeg")
print("Height:", image.shape[0], "Width:", image.shape[1])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]

cv2.imshow("THRESH", thresh)
cv2.waitKey(0)
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)
output = image.copy()

cv2.drawContours(image, [c], -1, (0, 255, 0), 10)
(x, yCoord, w, h) = cv2.boundingRect(c)
text = "original, num_puts={}".format(len(c))
cv2.putText(output, text, (x, yCoord - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

print("[INFO] {}".format(text))
cv2.imshow("Original Contour", output)
cv2.waitKey(0)

for eps in np.linspace(0.001, 0.05, 10):
    perimeter = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, eps * perimeter, True)
    output = image.copy()

    cv2.drawContours(output, [approx], -1, (0, 0, 0), 3)
    text = "eps={:4f}, num_pts={}".format(eps, len(approx))
    cv2.putText(output, text, (x, yCoord - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

    print("[INFO] {}".format(text))
    # j print(approx)
    cv2.imshow("Approximated contour", output)
    cv2.waitKey(0)

    if eps == .05:
        square = approx
        # print(type(approx))
        currMax, currMin = 0, image.shape[1]
        data = []
        arr = np.array(data)
        # print(data)
        for i in square:
            for x, y in i:
                data = np.append(data, y)
        newMax = np.max(data)  # these are the lowest and highest points of the image
        newMin = np.min(data)

        topHalf = image.shape[1] - newMax
        bottomHalf = image.shape[1] - newMin
        # print(type(topHalf), type(bottomHalf), type(image.shape[1]))
        print(int(topHalf), int(bottomHalf))
        cropImage = output[int(topHalf): int(bottomHalf), 0: int(image.shape[1])]
        # cropImage = output[int(newMin) - 40: int(newMax), 0: int(image.shape[1])]
        cv2.imshow("Cropped image", cropImage)
        cv2.waitKey(0)

    # print(findMax, findMin)
    # newMax = np.max(data)
    # must only get in the first spot not the second location
    # newMin = np.min(data)
    # print(newMax, newMin)
    # for x, y in i:  # can probably simplify this
    #    if currMax == x:
    #        cropX = image.shape[0] - currMin
    #    if currMin == y:
    #        cropY = image.shape[1] - currMax
    #    print(cropX, cropY)
    # print(x, y)

    # TODO
    # need to get the max and min of the coordinates and then crop the image
    # to the get the general shape of the coordinates
