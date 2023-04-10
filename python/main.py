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


def execute_embed_dct_dwt(alpha) -> None:
    original_image = cv2.imread('lnea.png', cv2.IMREAD_GRAYSCALE)
    original_watermark = cv2.imread('watermark_32.png', cv2.IMREAD_GRAYSCALE)
    result = dct_dwt.embed_watermark(image=original_image, watermark=original_watermark, alpha=alpha, seed1=10,
                                     seed2=20)

    cv2.imwrite('watermarked_dct_dwt.png', result)

    plt.figure('imaginea rezultată')
    plt.imshow(result, cmap='gray')
    plt.show()
    return


def execute_extract_dct_dwt() -> None:
    watermarked_image = cv2.imread('watermarked_dct_dwt.png', cv2.IMREAD_GRAYSCALE)
    original_image = cv2.imread('lnea.jpg', cv2.IMREAD_GRAYSCALE)
    original_watermark = cv2.imread('watermark_32.png', cv2.IMREAD_GRAYSCALE)
    original_watermark = dct_dwt.to_binary(original_watermark)

    result = dct_dwt.extract_watermark(original_image=original_image, watermarked_image=watermarked_image, seed1=10,
                                       seed2=20, alpha=25)

    plt.figure('extracted watermark result')
    plt.imshow(result, cmap='gray')
    plt.figure('original watermark')
    plt.imshow(original_watermark, cmap='gray')
    plt.show()

    mse = np.mean((original_watermark - result) ** 2)
    print('mse = ', mse)

    return


def execute_jpeg(key: int) -> None:
    original_image = cv2.imread('lnea.jpg', cv2.IMREAD_GRAYSCALE)
    original_watermark = cv2.imread('bgd_tdr.png', cv2.IMREAD_GRAYSCALE)
    original_watermark = dct_dwt.to_binary(original_watermark)
    result = helper.embed_watermark(original_watermark, original_image, key)
    cv2.imwrite('watermark_jpeg.png', result)
    plt.figure('imaginea rezultată')
    plt.imshow(result, cmap='gray')
    plt.show()


def extract_jpeg(key: int) -> None:
    image = cv2.imread('watermark_jpeg.png', cv2.IMREAD_GRAYSCALE)
    extracted_watermark = helper.extract_watermark(image, key)
    plt.figure('extracted watermark result')
    plt.imshow(extracted_watermark, cmap='gray')
    plt.show()


def execute_own_embed() -> None:
    original_image = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
    original_watermark = cv2.imread('watermark_32.png', cv2.IMREAD_GRAYSCALE)
    result = own.embed_watermark(key1=11, key2=12, key3=13, key4=14, image=original_image, watermark=original_watermark,
                                 alpha=50)

    cv2.imwrite('watermarked_own.png', result)
    plt.figure('imaginea rezultată')
    plt.imshow(result, cmap='gray')
    plt.show()
    return


def execute_own_extract() -> None:
    original_image = cv2.imread('lena.png', cv2.IMREAD_GRAYSCALE)
    watermarked_image = cv2.imread('watermarked_own.png', cv2.IMREAD_GRAYSCALE)

    print('mse = ',np.mean((np.array(original_image, dtype=np.float32) - np.array(watermarked_image, dtype=np.float32)) ** 2))
    result = own.extract_watermark(key1=11, key2=12, key3=13, original_image=original_image, image=watermarked_image)
    plt.figure('extracted image')
    plt.imshow(result, cmap='gray')
    plt.show()
    return


def calculate_psnr(img1, img2, max_value=255):
    """"Calculating peak signal-to-noise ratio (PSNR) between two images."""
    mse = np.mean((np.array(img1, dtype=np.float32) - np.array(img2, dtype=np.float32)) ** 2)
    if mse == 0:
        return 100
    return 20 * np.log10(max_value / (np.sqrt(mse)))

# region DCT_DWT
# execute_embed_dct_dwt(25)
# execute_extract_dct_dwt()
# endregion

#region DCT_JPEG
# execute_jpeg(2)
# original_image = cv2.imread('lnea.jpg', cv2.IMREAD_GRAYSCALE)
# watermakerd_image = cv2.imread('watermark_jpeg.png', cv2.IMREAD_GRAYSCALE)
# print('psnr = ', calculate_psnr(original_image, watermakerd_image))
# print('mse = ', np.mean((np.array(original_image, dtype=np.float32) - np.array(watermakerd_image, dtype=np.float32)) ** 2))

# extract_jpeg(2)
#endreagion

# execute_own_embed()
execute_own_extract()