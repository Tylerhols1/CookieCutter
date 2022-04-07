import cv2 as cv
import imutils


def shape_detector(contour):
    shape = ""

    # Arclength: calculates a contour perimeter or curve length
    # cv2.arcLength(curve, closed)
    contour_perimeter = cv.arcLength(contour, True)

    # ApproxPolyDP: Approximates a polygonal curve(s) with specified precision
    # cv2.approxPolyDP(curve, e, closed[curve])
    approx_poly_curve = cv.approxPolyDP(contour, 0.04 * contour_perimeter, True)

    if len(approx_poly_curve) == 3:
        shape = "triangle"
    elif len(approx_poly_curve) == 4:
        # Calculate the up right bounding triangle
        (x, y, w, h) = cv.boundingRect(approx_poly_curve)

        # Aspect Ratio between width and height
        aspect_ratio = w / float(h)

        if 0.95 < aspect_ratio < 1.05:
            shape = "square"
        else:
            shape = "rectangle"
    elif len(approx_poly_curve) == 5:
        shape = "pentagon"
    elif 5 < len(approx_poly_curve) < 8:
        shape = str(len(approx_poly_curve)) + "-gon"
    else:
        shape = "circle"
    return shape


# Load our image
image = cv.imread("/Users/tylerholstein/Documents/Fun Code/CookieCutter/berserkPanel.jpeg")

# Convert the image into grayscale
# cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# Apply the Gaussian blur to the gray image
# cv2.gaussianBlur(gray_image, kernel_size, sigmaX)
# sigmaX: Standard deviation of kernel along horizontal direction
# blur = cv.GaussianBlur(gray, (5, 5), 0)
# cv.imshow("Blur", blur)
# cv.waitKey(0)

# Find the threshold
# Thresholding is the binarization of an image
# cv2.threshold(blurred_image, T, out_value, method)
# T: Threshold value. All pixels <= T are set to 0 and
# all pixels >= T are set to 255
# out_value: The output value of pixels greater than T
# method: Our selected threshold method (Binary)
ret, thresh = cv.threshold(gray, 60, 255, cv.THRESH_BINARY)
cv.imshow("Thresh", thresh)
cv.waitKey(0)

# Find all contours in an image
# contours = cv.findContours(threshold.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# thresh.copy(): copy of threshold image from previous step
# cv.RETR_EXTERNAL: Detect only the parent contours. Ignore any of the child contours
# cv.CHAIN_APPROX: Leaves only the end points. Any point along the contour path will
# be dismissed leaving only the desired ones.
contours = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
cv.drawContours(image, contours, 3, (0, 0, 255), 8)

# Find the center of each contour
cnt = contours[0]
M = cv.moments(cnt)
if M['m00'] != 0:
    cx = int(M['m10'] / M['m00'])
    cy = int(M["m01"] / M['m00'])

    shape = shape_detector(cnt)

    cv.putText(image, shape, (cx, cy), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 4)

cv.imshow("Grayscale", gray)
cv.waitKey(0)

# display the image
cv.imshow("shapes", image)
cv.waitKey(0)
