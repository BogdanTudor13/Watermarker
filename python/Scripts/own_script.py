from helpers import dct_jpeg_qt_helpers as helper
from helpers import dct_dwt_helpers as dct_dwt
from helpers import own_helper as own
import numpy as np
import cv2
import pywt
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
from skimage import io as sio
import skimage
from helpers import helpers as h

original_image = cv2.imread('baboon.png', cv2.IMREAD_GRAYSCALE)
original_watermark = cv2.imread('watermark_32.png', cv2.IMREAD_GRAYSCALE)
watermark_binary = helper.to_binary(original_watermark)
output_image = cv2.imread('output.png', cv2.IMREAD_GRAYSCALE)


result = own.embed_watermark(key1=11, key2=12, key3=13, key4=10, image=original_image,
                             watermark=original_watermark)

if result is None:
    print('no image due to errors')
else:
    plt.figure()
    plt.imshow(result, cmap='gray')
    result = (result - np.min(result)) / (np.max(result) - np.min(result))
    sio.imsave('own.tif', result.astype(np.float64))
    cv2.imwrite('watermarked_dct_dwt.png', result)

normed_original_image = (original_image - np.min(original_image)) / (np.max(original_image) - np.min(original_image))
err = h.mse(normed_original_image, result)
print(err)

plt.figure()
plt.imshow(result, cmap='gray')


watermarked_image = cv2.imread('watermarked_dct_dwt.png', cv2.IMREAD_GRAYSCALE)
watermarked_image = sio.imread('own.tif')


watermark_reconstructed = own.extract_watermark(image=watermarked_image, key1=11, key2=12, key3=13, key4=10)
plt.figure()
plt.imshow(watermark_reconstructed, cmap='gray')
plt.show()

# myMatrix = np.array([[-0.71, 0.75, -0.04, 1.34], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
#
# (cA, (cH, cV, cD)) = pywt.dwt2(myMatrix, wavelet='haar')
#
# dct = cv2.dct(cV.astype('float32'))
#
# idct = cv2.idct(dct)
# img = pywt.idwt2((cA, (cH, idct, cD)), wavelet='haar')
#
#
# print(myMatrix)
# print(img)
