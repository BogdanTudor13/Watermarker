import numpy as np
import cv2

jpeg_luminance_qt = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                              [12, 12, 14, 19, 26, 58, 60, 55],
                              [14, 13, 16, 24, 40, 57, 69, 56],
                              [14, 17, 22, 29, 51, 87, 80, 62],
                              [18, 22, 37, 56, 68, 109, 103, 77],
                              [24, 35, 55, 64, 81, 104, 113, 92],
                              [49, 64, 78, 87, 103, 121, 120, 101],
                              [72, 92, 95, 98, 112, 100, 103, 99]
                              ])

jpeg_color_qt = np.array([[17, 18, 24, 47, 99, 99, 99, 99],
                          [18, 21, 26, 66, 99, 99, 99, 99],
                          [24, 26, 56, 99, 99, 99, 99, 99],
                          [47, 66, 99, 99, 99, 99, 99, 99],
                          [99, 99, 99, 99, 99, 99, 99, 99],
                          [99, 99, 99, 99, 99, 99, 99, 99],
                          [99, 99, 99, 99, 99, 99, 99, 99],
                          [99, 99, 99, 99, 99, 99, 99, 99]
                          ])

webber_ratio = 0.02

I1 = 80

I2 = 160

pairs = [[(0, 2), (2, 1)]]

a = 1

b = 8

c = 10

d = 20


def scramble_pixels(x, y, n):
    current_position = np.array([[x], [y]])
    const_window = np.array([[1, 1], [1, 2]])

    return np.matmul(const_window, current_position) % n


def to_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray


def arnold_transform(image, key):
    (m, n, _) = image.shape
    scrambled_image = np.zeros(image.shape)
    for k in range(0, key):
        for x in range(0, n):
            for y in range(0, n):
                new_positions = scramble_pixels(x, y, n)
                scrambled_image[new_positions[0], new_positions[1]] = image[x, y]

    return scrambled_image


def image_8_x_8_division(image):
    blocks = []
    m, n = image.shape
    for i in range(7, n - 1, 8):
        for j in range(7, m - 1, 8):
            blocks.append(image[i - 8 + 1:i][j - 8 + 1:j])

    return blocks


def get_adaptive_adjustment_coefficient(block):
    beta = get_beta(block)
    ave = np.average(block)
    w = webber_ratio
    if ave < I1:
        w = ((beta - webber_ratio) * pow((ave - I1), 2)) / (I2 * I2) + webber_ratio
    if ave >= I2:
        w = ((beta - webber_ratio) * pow((ave - I2), 2)) / pow((255 - I2), 2) + webber_ratio
    return w


def get_entropy(block):
    Ent = 0
    # calculate entropy and ajust it to [a,b]
    return None


def embed_watermark(watermark, image, key):
    scrambled_watermark = arnold_transform(watermark, key)
    blocks = image_8_x_8_division(image)

    return None



def get_masking_factor(image):
    return None


def get_beta(image):
    return np.amax(image) - np.amin(image)
