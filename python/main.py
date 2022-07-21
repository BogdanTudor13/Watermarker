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


watermark = cv2.imread('watermark_gray.png')

gray = helper.to_gray(watermark)


print(gray.shape)