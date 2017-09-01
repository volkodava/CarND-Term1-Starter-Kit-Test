import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

exp_image = mpimg.imread('exit_ramp_edges.jpg')
# Read in the image and convert to grayscale
image = mpimg.imread('exit-ramp.jpg')
# Define a kernel size for Gaussian smoothing / blurring
# Note: this step is optional as cv2.Canny() applies a 5x5 Gaussian internally
kernel_size = 15
# Define parameters for Canny and run it
# NOTE: if you try running this code you might want to change these!
low_threshold = 23
high_threshold = 46


def show_image():
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.xticks(())
    plt.yticks(())
    plt.imshow(edges, cmap='gray')
    plt.title('Solution')

    plt.subplot(2, 2, 2)
    plt.xticks(())
    plt.yticks(())
    plt.imshow(exp_image, cmap='gray')
    plt.title('Expected')

    plt.subplot(2, 2, 3)
    plt.xticks(())
    plt.yticks(())
    plt.imshow(gray, cmap='gray')
    plt.title('Gray')

    plt.subplot(2, 2, 4)
    plt.xticks(())
    plt.yticks(())
    plt.imshow(blur_gray, cmap='gray')
    plt.title('Blur')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print('This image is: ', type(image),
          'with dimensions:', image.shape)
    show_image()
