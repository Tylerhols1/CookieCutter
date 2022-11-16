def gui_panel():
    # TODO look into tkinter
    # add images to buttons in tkinter
    window = Tk()
    Label(window, text="window", font=("Courier New", 15)).pack(side=TOP, pady=10)
    photo = PhotoImage(file=r"images/batman01.png")
    photoimage = photo.subsample(3, 3)
    Button(window, image=photoimage, compound=LEFT).pack(side=TOP, pady=10)
    mainloop()