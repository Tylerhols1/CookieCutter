def create_collage():
    """

    Returns
    -------
    NONE
    """
    img1 = Img.open(r"cropped/cropped_0_hulk01.jpg").convert('RGB')
    img2 = Img.open(r"cropped/cropped_0_alita01.jpg")
    x, y = img1.size
    print(img1.mode, img2.mode)
    img1.paste(img2, (0, 0))
    img1.show()