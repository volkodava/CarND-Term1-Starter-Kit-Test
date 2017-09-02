import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

# Read in and grayscale the image
image = mpimg.imread('exit-ramp.jpg')
# Define a kernel size and apply Gaussian smoothing
kernel_size = 5
# Define our parameters for Canny and apply
low_threshold = 50
high_threshold = 150
# Next we'll create a masked edges image using cv2.fillPoly()
imshape = image.shape
start_point = (420, 300)
p1 = start_point
p2 = (525, 300)
p3 = (910, imshape[0])
p4 = (50, imshape[0])
p5 = start_point
vertices = np.array([[p1, p2, p3, p4]], dtype=np.int32)
# vertices = np.array([[(0,imshape[0]),(0, 0), (imshape[1], 0), (imshape[1],imshape[0])]], dtype=np.int32)
# Define the Hough transform parameters
# Make a blank the same size as our image to draw on
rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 1  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 5  # minimum number of pixels making up a line
max_line_gap = 1  # maximum gap in pixels between connectable line segments


def plot(image, xx, yy):
    plt.plot(xx, yy, 'b--', lw=4)
    plt.imshow(image)
    plt.show()


def draw_one(one, one_title="No Title"):
    plt.imshow(one)
    plt.title(one_title)
    plt.show()


def draw_four(one, one_title, two, two_title, three, three_title, four, four_title):
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.xticks(())
    plt.yticks(())
    plt.imshow(one)
    plt.title(one_title)

    plt.subplot(2, 2, 2)
    plt.xticks(())
    plt.yticks(())
    plt.imshow(two)
    plt.title(two_title)

    plt.subplot(2, 2, 3)
    plt.xticks(())
    plt.yticks(())
    plt.imshow(three)
    plt.title(three_title)

    plt.subplot(2, 2, 4)
    plt.xticks(())
    plt.yticks(())
    plt.imshow(four)
    plt.title(four_title)

    plt.tight_layout()
    plt.show()


def show_image():
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    # Next we'll create a masked edges image using cv2.fillPoly()
    mask = np.zeros_like(edges)
    ignore_mask_color = 255

    # This time we are defining a four sided polygon to mask
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_edges = cv2.bitwise_and(edges, mask)
    # draw_one(masked_edges)
    print("vertices = np.array([[%s,%s,%s,%s]], dtype=np.int32)" % (p1, p2, p3, p4))
    plot(image, (p1[0], p2[0], p3[0], p4[0], p5[0]), (p1[1], p2[1], p3[1], p4[1], p5[1]))

    line_image = np.copy(image) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    # Iterate over the output "lines" and draw lines on a blank image
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

    # Create a "color" binary image to combine with line image
    color_edges = np.dstack((edges, edges, edges))

    # Draw the lines on the edge image
    lines_edges = cv2.addWeighted(color_edges, 0.8, line_image, 1, 0)


if __name__ == "__main__":
    print('This image is: ', type(image),
          'with dimensions:', image.shape)
    show_image()
