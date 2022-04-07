import cv2
import numpy as np

image = cv2.imread('/Users/tylerholstein/Documents/Fun Code/CookieCutter/square.jpeg')
print(image.shape)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)


harris_corners = cv2.cornerHarris(gray, 3, 3, 0.05)

kernel = np.ones((7, 7), np.uint8)

harris_corners = cv2.dilate(harris_corners, kernel, iterations=2)

image[harris_corners > 0.025 * harris_corners.max()] = [255, 127, 127]

cv2.imshow('Harris Corners', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
