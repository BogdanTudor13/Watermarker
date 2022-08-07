from helpers import dct_jpeg_qt_helpers as helper
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

original_image = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
origianl_watermark = cv2.imread('bgd_tdr.png', cv2.IMREAD_GRAYSCALE)
watermark_binary = helper.to_binary(origianl_watermark)
output_image = cv2.imread('output.png', cv2.IMREAD_GRAYSCALE)
numbered_key = 12


def exec_embeding(image, watermark, key):
    result = helper.embed_watermark(watermark, image, key)
    cv2.imwrite('output.png', result)

    return None


def exec_extracting(image, key):
    result = helper.extract_watermark(embeded_image=image, k=key)
    result = result * 255

    cv2.imwrite('extracted_wmk.png', result)
    return None


# exec_embeding(original_image, watermark_binary, 7)
exec_extracting(image=output_image, key=7)

# matrix = np.array([[1, 2], [3, 4]])
# arnold = helper.arnold_transform(matrix, 2)
# print(arnold)
# reverse = helper.reverse_arnold(arnold, 2)
# print(reverse)
