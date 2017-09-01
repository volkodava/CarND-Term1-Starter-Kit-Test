import os
from tkinter import Canvas, Button, Frame, Tk, Scale, HORIZONTAL, Image, IntVar, OptionMenu, Radiobutton
from tkinter.filedialog import askopenfilename

import cv2
import matplotlib.image as mpimg
import numpy as np
from PIL import Image, ImageTk


class ImageToolUi(Tk):
    fileTypes = [('JPG files', '*.jpg'), ('All files', '*')]
    kernelOptions = [i for i in range(1, 50, 2)]

    def __init__(self):
        Tk.__init__(self)

        self.image_path = None
        self.kernel_value = 13
        self.low_threshold_value = 15
        self.high_threshold_value = 30
        self.img_path = None
        self.numpy_image = None
        self.low_to_high_multiplier = 1

        # create ui
        f = Frame(self, bd=2)

        self.openImageButton = Button(f, text='Open Image',
                                      command=self.open_image)
        self.openImageButton.pack(side='left')

        self.kernel = IntVar(self)
        self.kernel.set(self.kernelOptions[0])
        self.kernelMenu = OptionMenu(f, self.kernel, *self.kernelOptions, command=self.on_kernel)
        self.kernelMenu.config(width=5)
        self.kernelMenu.pack(side='left')

        self.low_threshold_var = IntVar()
        self.low_threshold_var.set(1)
        self.low_threshold = Scale(f, label='Low Threshold', orient=HORIZONTAL, from_=1, to=255,
                                   variable=self.low_threshold_var, command=self.on_low_threshold)
        self.low_threshold.pack(side='left')

        self.high_threshold_var = IntVar()
        self.high_threshold_var.set(1)
        self.high_threshold = Scale(f, label='High Threshold', orient=HORIZONTAL, from_=1, to=255,
                                    variable=self.high_threshold_var, command=self.on_high_threshold)
        self.high_threshold.pack(side='left')

        self.relation_var = IntVar()
        self.relation_var.set(self.low_to_high_multiplier)
        self.one_to_one = Radiobutton(f, text="1 to 1", variable=self.relation_var, value=1, command=self.on_relation)
        self.one_to_one.pack(side='left')
        self.one_to_two = Radiobutton(f, text="1 to 2", variable=self.relation_var, value=2, command=self.on_relation)
        self.one_to_two.pack(side='left')
        self.one_to_three = Radiobutton(f, text="1 to 3", variable=self.relation_var, value=3, command=self.on_relation)
        self.one_to_three.pack(side='left')

        f.pack(fill='x')

        self.c = Canvas(self, bd=0, highlightthickness=0,
                        width=100, height=100)
        self.c.pack(fill='both', expand=1)

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.load_image(os.path.join(cur_dir, "Canny to Detect Lane Lines", "exit-ramp.jpg"))

    def open_image(self):
        file = askopenfilename(filetypes=self.fileTypes)
        if file:
            self.load_image(file)

    def load_image(self, path):
        self.img_path = path
        self.numpy_image = mpimg.imread(path)
        self.reload_image(self.numpy_image)

    def reload_image(self, numpy_image):
        im = Image.fromarray(numpy_image)
        # im = Image.open(path)
        # im.thumbnail((1024, 768))

        self.tkphoto = ImageTk.PhotoImage(im)
        self.canvasItem = self.c.create_image(0, 0, anchor='nw', image=self.tkphoto)
        self.c.config(width=im.size[0], height=im.size[1])

    def on_kernel(self, value):
        self.kernel_value = value

        if self.numpy_image is not None:
            print("Set kernel to: ", self.kernel_value)
            self.update_image(np.copy(self.numpy_image))

    def on_low_threshold(self, value):
        self.low_threshold_value = int(value)
        self.high_threshold_value = self.low_threshold_value * int(self.low_to_high_multiplier)
        self.high_threshold_var.set(self.high_threshold_value)

        if self.numpy_image is not None:
            print("Set low_threshold to: ", self.low_threshold_value)
            self.update_image(np.copy(self.numpy_image))

    def on_high_threshold(self, value):
        self.high_threshold_value = int(value)
        self.low_threshold_value = self.high_threshold_value / int(self.low_to_high_multiplier)
        self.low_threshold_var.set(self.low_threshold_value)

        if self.numpy_image is not None:
            print("Set high_threshold to: ", self.high_threshold_value)
            self.update_image(np.copy(self.numpy_image))

    def on_relation(self):
        if self.relation_var.get():
            self.low_to_high_multiplier = self.relation_var.get()

    def update_image(self, tmp_image):
        gray = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
        blur_gray = cv2.GaussianBlur(gray, (int(self.kernel_value), int(self.kernel_value)), 0)
        edges = cv2.Canny(blur_gray, float(self.low_threshold_value), float(self.high_threshold_value))
        # path, file = os.path.split(self.img_path)
        # new_file_path = os.path.join(path, "tmp_" + file)
        # mpimg.imsave(new_file_path, edges)
        # print("Processed image stored: ", new_file_path)
        self.reload_image(edges)


if __name__ == "__main__":
    app = ImageToolUi()
    app.mainloop()
