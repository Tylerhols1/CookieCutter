# CookieCutter

___

### *What is it?*

CookieCutter is a program that takes comic/manga images and extracts one panel from that image, crops it, and then saves
as a new image.

* Access images from the /images/ directory
* Takes that image, converts it to grayscale, and then sends through threshold
* Take the threshold image and approximates a shape from the image's contours
* When the approximated shape is enough to crop a new image, it then saves a new cropped image to the /cropped/
  directory

### *Inspiration for this project*

I recently got into the raspberry pi and was **super** excited to see what I could do with the raspberry pi myself.
Well, one day I was on the [**raspberry pi website**](https://www.raspberrypi.com) and was looking at the products and I
stumbled upon the 'news' tab on the site and was just looking at the various projects that people have come up with. I
came across [**this**](https://www.raspberrypi.com/news/systemsix-a-love-letter-letter-to-old-macs-for-your-desk/)
amazing project that displays accurate weather updates and your own apple calendar. Such a cool project and such an
awesome idea that incorporates an E-reader display 
