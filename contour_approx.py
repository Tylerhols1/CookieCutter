from PIL import Image
import imutils
import cv2
import numpy as np

new_mask = 0


def create_collage():
    img1 = Image.open(r"guts_02.jpeg").convert('RGB')
    img2 = Image.open(r"berserkPanel.jpeg")
    x, y = img1.size
    print(img1.mode, img2.mode)
    img1.paste(img2, (0, 0))
    img1.show()


def image_show(image, window_text):
    cv2.imshow("{}".format(window_text), image)
    cv2.waitKey(0)


def initialize_image():
    image = cv2.imread(r"guts_01.png")
    image_show(image, "Original Pic")

    print("Height:", image.shape[0], "Width:", image.shape[1])
    thresh_image(image, 0)
    # could try cropping the photo so it has to pick a different panel
    # canny = cv2.Canny(image, 149, 150)  ## try this instead of thresh


def thresh_image(image, i):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_show(gray, "GRAY")
    ret, thresh = cv2.threshold(gray, 155, 255, i)
    image_show(thresh, "Thresh")
    find_contour(image, thresh)


def find_contour(image, thresh):
    global new_mask
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)  # changing the panels has to come from this variable cnts

    print(cv2.contourArea)
    c = max(cnts, key=cv2.contourArea)

    output = image.copy()

    cv2.drawContours(output, [c], -1, (0, 255, 0), 10)
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
        image_show(output, "Approximated contour")

        if eps == .05:  # could look at changing this to check for the number of points
            dataY = []
            np.array(dataY)
            print(approx)

            for i in approx:
                for x, y in i:
                    dataY = np.append(dataY, y)
            print("data numpy array with", dataY)

            maxY = np.max(dataY)  # these are the lowest and highest points of the image
            minY = np.min(dataY)

            print("MaxY and MinY", maxY, minY)
            if maxY == 0 or maxY < minY:
                cv2.destroyAllWindows()
                new_mask = new_mask + 1
                thresh_image(image, new_mask)

            elif int(image.shape[0]) - 10 <= maxY <= int(image.shape[0]):
                cv2.destroyAllWindows()
                new_mask = new_mask + 1
                thresh_image(image, new_mask)

            elif int(image.shape[1]) - 10 <= maxY <= int(image.shape[1]):
                cv2.destroyAllWindows()
                new_mask = new_mask + 1
                thresh_image(image, new_mask)
                
            else:
                # cv2.destroyAllWindows()
                # new_mask = new_mask + 1
                # thresh_image(image, new_mask)
                crop_image = image[int(minY): int(maxY), 0: int(image.shape[1])]
                print(crop_image)
                image_show(crop_image, "Cropped image")


def main():
    # create_collage()
    initialize_image()


if __name__ == '__main__':
    main()
