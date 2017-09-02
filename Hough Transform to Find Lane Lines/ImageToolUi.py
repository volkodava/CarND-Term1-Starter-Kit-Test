import os
from tkinter import Canvas, Button, Frame, Tk, Scale, HORIZONTAL, Image, IntVar
from tkinter.filedialog import askopenfilename

import cv2
import matplotlib.image as mpimg
import numpy as np
from PIL import Image, ImageTk, ImageDraw


class ImageToolUi(Tk):
    fileTypes = [('JPG files', '*.jpg'), ('All files', '*')]
    kernelOptions = [i for i in range(1, 50, 2)]

    def __init__(self):
        Tk.__init__(self)

        self.img_path = None
        self.numpy_image = None

        # INPUT PARAMETERS
        self.kernel_size = 5
        self.low_threshold = 50
        self.high_threshold = 150
        self.p1 = None
        self.p2 = None
        self.p3 = None
        self.p4 = None
        self.p5 = None
        self.vertices = None
        # TO DEFINE PARAMETERS
        # distance resolution in pixels of the Hough grid
        self.rho = 1
        # angular resolution in radians of the Hough grid
        self.selected_degree = 3
        self.theta = self.selected_degree * np.pi / 180
        # minimum number of votes (intersections in Hough grid cell)
        self.threshold = 30
        # minimum number of pixels making up a line
        self.min_line_length = 25
        # maximum gap in pixels between connectable line segments
        self.max_line_gap = 30

        # create ui
        f = Frame(self, bd=2)

        Button(f, text='Open Image',
               command=self.open_image).pack(side='left')

        Button(f, text='Rectangle',
               command=self.on_rect).pack(side='left')

        self.rho_var = IntVar()
        self.rho_var.set(self.rho)
        Scale(f, label='Rho', orient=HORIZONTAL, from_=1, to=100,
              variable=self.rho_var, command=self.on_rho).pack(side='left')

        self.theta_var = IntVar()
        self.theta_var.set(self.selected_degree)
        Scale(f, label='Theta', orient=HORIZONTAL, from_=1, to=60,
              variable=self.theta_var, command=self.on_theta).pack(side='left')

        self.votes_var = IntVar()
        self.votes_var.set(self.threshold)
        Scale(f, label='Votes', orient=HORIZONTAL, from_=1, to=100,
              variable=self.votes_var, command=self.on_votes).pack(side='left')

        self.min_line_var = IntVar()
        self.min_line_var.set(self.min_line_length)
        Scale(f, label='Min Length', orient=HORIZONTAL, from_=1, to=100,
              variable=self.min_line_var, command=self.on_min_line).pack(side='left')

        self.max_line_var = IntVar()
        self.max_line_var.set(self.max_line_gap)
        Scale(f, label='Max Gap', orient=HORIZONTAL, from_=1, to=100,
              variable=self.max_line_var, command=self.on_max_line).pack(side='left')

        Button(f, text='Print',
               command=self.on_print).pack(side='left')

        f.pack(fill='x')

        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                             width=100, height=100)
        self.canvas.pack(fill='both', expand=1)

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.load_image(os.path.join(cur_dir, "exit-ramp.jpg"))

    def open_image(self):
        file = askopenfilename(filetypes=self.fileTypes)
        if file:
            self.load_image(file)

    def load_image(self, path):
        self.img_path = path
        self.numpy_image = mpimg.imread(path)
        self.reload_image(self.numpy_image)

    def reload_image(self, numpy_image):
        imshape = numpy_image.shape

        start_point = (420, 300)
        self.p1 = start_point
        self.p2 = (525, 300)
        self.p3 = (910, imshape[0])
        self.p4 = (50, imshape[0])
        self.p5 = start_point
        self.vertices = np.array([[self.p1, self.p2, self.p3, self.p4]], dtype=np.int32)

        im = Image.fromarray(numpy_image)
        # im = Image.open(path)
        # im.thumbnail((1024, 768))

        self.tkphoto = ImageTk.PhotoImage(im)
        self.canvasItem = self.canvas.create_image(0, 0, anchor='nw', image=self.tkphoto)
        self.canvas.config(width=im.size[0], height=im.size[1])

    def update_image(self, tmp_image):
        gray = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
        blur_gray = cv2.GaussianBlur(gray, (self.kernel_size, self.kernel_size), 0)
        edges = cv2.Canny(blur_gray, self.low_threshold, self.high_threshold)

        # Next we'll create a masked edges image using cv2.fillPoly()
        mask = np.zeros_like(edges)
        ignore_mask_color = 255

        # This time we are defining a four sided polygon to mask
        cv2.fillPoly(mask, self.vertices, ignore_mask_color)
        masked_edges = cv2.bitwise_and(edges, mask)

        # creating a blank to draw lines on
        line_image = np.copy(tmp_image) * 0

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(masked_edges, self.rho, self.theta, self.threshold, np.array([]),
                                self.min_line_length, self.max_line_gap)

        # Iterate over the output "lines" and draw lines on a blank image
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

        # Create a "color" binary image to combine with line image
        color_edges = np.dstack((edges, edges, edges))

        # Draw the lines on the edge image
        lines_edges = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0)
        # path, file = os.path.split(self.img_path)
        # new_file_path = os.path.join(path, "tmp_" + file)
        # mpimg.imsave(new_file_path, lines_edges)
        # print("Processed image stored: ", new_file_path)
        self.reload_image(lines_edges)

    def on_moved(self, event):
        self.canvas.itemconfigure(self.canvas_tag, text="(%r, %r)" % (event.x, event.y))

    def on_rect(self):
        if self.numpy_image is not None:
            im = Image.fromarray(np.copy(self.numpy_image))

            draw = ImageDraw.Draw(im)
            draw.line([self.p1, self.p2, self.p3, self.p4, self.p5], width=2)

            self.tkphoto = ImageTk.PhotoImage(im)
            self.canvasItem = self.canvas.create_image(0, 0, anchor='nw', image=self.tkphoto)
            self.canvas.config(width=im.size[0], height=im.size[1])

            self.canvas.bind("<Motion>", func=self.on_moved)
            self.canvas_tag = self.canvas.create_text(10, 10, text="", anchor="nw", fill="yellow")

    def on_rho(self, value):
        self.rho = int(value)

        if self.numpy_image is not None:
            print("Set rho to: ", self.rho)
            self.update_image(np.copy(self.numpy_image))

    def on_theta(self, value):
        self.selected_degree = int(value)
        self.theta = self.selected_degree * np.pi / 180

        if self.numpy_image is not None:
            print("Set selected_degree to: ", self.selected_degree)
            print("Set theta to: ", self.theta)
            self.update_image(np.copy(self.numpy_image))

    def on_votes(self, value):
        self.threshold = int(value)

        if self.numpy_image is not None:
            print("Set threshold (votes) to: ", self.threshold)
            self.update_image(np.copy(self.numpy_image))

    def on_min_line(self, value):
        self.min_line_length = int(value)

        if self.numpy_image is not None:
            print("Set min_line_length to: ", self.min_line_length)
            self.update_image(np.copy(self.numpy_image))

    def on_max_line(self, value):
        self.max_line_gap = int(value)

        if self.numpy_image is not None:
            print("Set max_line_gap to: ", self.max_line_gap)
            self.update_image(np.copy(self.numpy_image))

    def on_print(self):
        print("""
...
vertices = np.array([[{p1},{p2},{p3},{p4}]], dtype=np.int32)
...
rho = {rho} # distance resolution in pixels of the Hough grid
theta = {degree} * np.pi/180 # angular resolution in radians of the Hough grid
threshold = {threshold} # minimum number of votes (intersections in Hough grid cell)
min_line_length = {min_line_length} # minimum number of pixels making up a line
max_line_gap = {max_line_gap} # maximum gap in pixels between connectable line segments
line_image = np.copy(image)*0 # creating a blank to draw lines on
...        
        """.format(p1=self.p1, p2=self.p2, p3=self.p3, p4=self.p4, rho=self.rho, degree=self.selected_degree,
                   threshold=self.threshold, min_line_length=self.min_line_length, max_line_gap=self.max_line_gap))


if __name__ == "__main__":
    app = ImageToolUi()
    app.mainloop()
