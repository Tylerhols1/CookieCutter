import cv2

# reading the image into image var using imread() function
image = cv2.imread("/Users/tylerholstein/Documents/Fun Code/CookieCutter/berserkPanel.jpeg")

# converts the image into grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# takes image var and inverts colors with canny
edges = cv2.Canny(gray, 30, 200)

# applying threshold to the image
# ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Finding the contours
# use a copy of the image
# since findContours alters the image

contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.boundingRect(contours)
cv2.imshow("Thresh", edges)
cv2.waitKey(0)

cnt = contours[4]
print([cnt])
cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
cv2.imshow("Contours", image)
cv2.waitKey(0)

# print(image.shape)
# cv2.imshow("Cropped", crop)
# cv2.waitKey(0)
cv2.destroyAllWindows()
