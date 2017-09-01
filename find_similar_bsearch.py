from collections import OrderedDict
from operator import itemgetter

import cv2
import matplotlib.image as mpimg
import numpy as np
from skimage.measure import compare_ssim as ssim


def search(lst, calc, prevResult):
    min = 0
    max = len(lst) - 1
    avg = int((min + max) / 2)

    while min < max:
        newResult = calc(lst[avg])

        if newResult > 0.99:
            return avg
        elif newResult >= prevResult:
            return avg + 1 + search(lst[avg + 1:], calc, newResult)
        else:
            return search(lst[:avg], calc, newResult)
    return avg


def color_comp(color_idx, rgb_threshold, sim_result_lst):
    def calc(intensity_lvl):
        image = mpimg.imread('test.jpg')
        color_select = np.copy(image)

        rgb_threshold[color_idx] = intensity_lvl

        thresholds = (image[:, :, 0] < rgb_threshold[0]) \
                     | (image[:, :, 1] < rgb_threshold[1]) \
                     | (image[:, :, 2] < rgb_threshold[2])
        color_select[thresholds] = [0, 0, 0]
        mpimg.imsave("test-result.jpg", color_select)

        result = cv2.imread("test-result.jpg")
        expected = cv2.imread("expected_result.jpg")
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        expected = cv2.cvtColor(expected, cv2.COLOR_BGR2GRAY)

        simValue = ssim(expected, result)
        sim_result_lst.append((intensity_lvl, simValue))

        return simValue

    return calc


def runColors():
    rgb_threshold = [0, 0, 0]
    color_names = {0: 'Red', 1: 'Green', 2: 'Blue'}
    colors = OrderedDict({0: [i for i in range(0, 256)], 1: [i for i in range(0, 256)], 2: [i for i in range(0, 256)]})
    result = []

    for color_idx, intensities in colors.items():

        start = 0
        end = len(intensities)
        max_found_lst = 0
        run = True
        while run:
            inputIntensities = intensities[start:end]

            sim_result_lst = []
            search(inputIntensities, color_comp(color_idx, rgb_threshold, sim_result_lst), 0)

            print(sim_result_lst)

            max_found_lst = max(sim_result_lst, key=itemgetter(1))
            if max_found_lst[1] < 0.99:
                sim_vals = [val[1] for val in sim_result_lst]
                res = [j - i for i, j in zip(sim_vals[:-1], sim_vals[1:])]
                intr_range = []

                for idx in range(len(res)):
                    if res[idx] > 0:
                        intr_range.append(idx)
                    else:
                        intr_range.append(idx)
                        break

                print(intr_range)

                if len(intr_range) > 1:
                    start = sim_result_lst[intr_range[-2]][0]
                    end = sim_result_lst[intr_range[-1]][0]
                else:
                    run = False

            else:
                run = False

        rgb_threshold[color_idx] = max_found_lst[0]
        result.append(max_found_lst[0])

        print("rgb_threshold: %s" % rgb_threshold)

    print(result)


if __name__ == "__main__":
    # runSimple()
    runColors()

    # # Read in the image
    # image = mpimg.imread('test.jpg')
    # color_select = np.copy(image)
    #
    # # Define color selection criteria
    # ###### MODIFY THESE VARIABLES TO MAKE YOUR COLOR SELECTION
    # red_threshold = 200
    # green_threshold = 200
    # blue_threshold = 200
    # ######
    #
    # rgb_threshold = [red_threshold, green_threshold, blue_threshold]
    # thresholds = (image[:, :, 0] < rgb_threshold[0]) \
    #              | (image[:, :, 1] < rgb_threshold[1]) \
    #              | (image[:, :, 2] < rgb_threshold[2])
    # color_select[thresholds] = [0, 0, 0]
    # mpimg.imsave("test-result.jpg", color_select)
    #
    # result = cv2.imread("test-result.jpg")
    # expected = cv2.imread("expected_result.jpg")
    # result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # expected = cv2.cvtColor(expected, cv2.COLOR_BGR2GRAY)
    #
    # print("ssim: %s" % ssim(expected, result))
