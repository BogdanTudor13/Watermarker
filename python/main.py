from helpers import dct_jpeg_qt_helpers as helper
from helpers import dct_dwt_helpers as dct_dwt
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib

original_image = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
original_watermark = cv2.imread('watermark_32.png', cv2.IMREAD_GRAYSCALE)
watermark_binary = helper.to_binary(original_watermark)
output_image = cv2.imread('output.png', cv2.IMREAD_GRAYSCALE)
alpha = 2
seed1 = 10
seed2 = 20
result = dct_dwt.embed_watermark(original_watermark, original_image, alpha, seed1, seed2)

if result is None:
    print('no image due to errors')
else:
    plt.figure()
    plt.imshow(result, cmap='gray')
    cv2.imwrite('watermarked_dct_dwt.png', result)

plt.figure()
plt.imshow(original_image, cmap='gray')
plt.show()

watermarked_image = cv2.imread('watermarked_dct_dwt.png', cv2.IMREAD_GRAYSCALE)
watermark_reconstructed = dct_dwt.extract_watermark(watermarked_image, seed1, seed2)
plt.figure()
plt.imshow(watermark_reconstructed, cmap='gray')
plt.show()