from helpers import dct_jpeg_qt_helpers as helper
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')


def test(x, y, n):
    current_position = np.array([[x], [y]])
    const_window = np.array([[1, 1], [1, 2]])

    return np.matmul(const_window, current_position) % n


watermark = cv2.imread('watermark_binary.jpg', cv2.IMREAD_GRAYSCALE)
lena = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
print(watermark.shape)
print(lena.shape)

test = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])

print(test)
print(np.amax(test))
print(np.amin(test))
print(np.average(test))