import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

img = Image.open('test.jpg')
new_img = img.resize((960, 540))
new_img.save("test_resized.jpg", "JPEG")

# Read in the image and print some stats
image = mpimg.imread('test_resized.jpg')
ysize = image.shape[0]
xsize = image.shape[1]
color_select = np.copy(image)
line_image = np.copy(image)
# Define our color criteria
red_threshold = 205
green_threshold = 205
blue_threshold = 205
rgb_threshold = [red_threshold, green_threshold, blue_threshold]
# Define a triangle region of interest (Note: if you run this code,
# Keep in mind the origin (x=0, y=0) is in the upper left in image processing
# you'll find these are not sensible values!!
# But you'll get a chance to play with them soon in a quiz ;)
left_bottom = [90, ysize]
right_bottom = [830, ysize]
apex = [480, 320]


def show_image():
    # Perform a linear fit (y=Ax+B) to each of the three sides of the triangle
    # np.polyfit returns the coefficients [A, B] of the fit
    fit_left = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), 1)
    fit_right = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), 1)
    fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)

    # Mask pixels below the threshold
    color_thresholds = (image[:, :, 0] < rgb_threshold[0]) | \
                       (image[:, :, 1] < rgb_threshold[1]) | \
                       (image[:, :, 2] < rgb_threshold[2])

    # Find the region inside the lines
    XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
    region_thresholds = (YY > (XX * fit_left[0] + fit_left[1])) & \
                        (YY > (XX * fit_right[0] + fit_right[1])) & \
                        (YY < (XX * fit_bottom[0] + fit_bottom[1]))

    # Mask color and region selection
    color_select[color_thresholds | ~region_thresholds] = [0, 0, 0]
    # Color pixels red where both color and region selections met
    line_image[~color_thresholds & region_thresholds] = [255, 0, 0]

    # Display the image and show region and color selections
    plt.imshow(image)
    x = [left_bottom[0], right_bottom[0], apex[0], left_bottom[0]]
    y = [left_bottom[1], right_bottom[1], apex[1], left_bottom[1]]
    plt.plot(x, y, 'b--', lw=4)
    plt.imshow(color_select)
    plt.imshow(line_image, extent=[XX.min(), XX.max(), YY.max(), YY.min()])
    plt.show()


if __name__ == "__main__":
    print('This image is: ', type(image),
          'with dimensions:', image.shape)
    show_image()
