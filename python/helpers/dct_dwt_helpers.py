import numpy as np
import cv2
import pywt
import random


#                             -------------------
#                             |        |        |
#                             | cA(LL) | cH(LH) |
#                             |        |        |
# (cA, (cH, cV, cD))  <--->   -------------------
#                             |        |        |
#                             | cV(HL) | cD(HH) |
#                             |        |        |
#                             -------------------

def embed_watermark(watermark, image, alpha, seed1, seed2):
    dct_blocks = []
    (cA, (cH, cV, cD)) = pywt.dwt2(image, wavelet='haar')
    (cA2, (cH2, cV2, cD2)) = pywt.dwt2(cV, wavelet='haar')

    blocks = image_4_x_4_division(cV2)
    dct_blocks = apply_dct_to_blocks(blocks)
    binary_watermark = to_binary(watermark)
    pn0, pn1 = generate_pseudorandom_sequences(seed1=seed1, seed2=seed2, length=4)
    dct_blocks = embed_pseudorandom_sequences(dct_blocks, pn0, pn1, binary_watermark, alpha)
    if dct_blocks is None:
        return None
    idct_blocks = apply_idct_to_blocks(dct_blocks)

    embeded_img = reshape_4_x_4_blocks_to_image(idct_blocks, cH2.shape[0])

    cH = pywt.idwt2((cA2, (cH2, embeded_img, cD2)), wavelet='haar')
    watermarked_img = pywt.idwt2((cA, (cH, cV, cD)), wavelet='haar')
    return watermarked_img


def extract_watermark(image, seed1, seed2):
    dct_blocks = []
    (cA, (cH, cV, cD)) = pywt.dwt2(image, wavelet='haar')
    (cA2, (cH2, cV2, cD2)) = pywt.dwt2(cH, wavelet='haar')
    blocks = image_4_x_4_division(cH2)

    pn0, pn1 = generate_pseudorandom_sequences(seed1=seed1, seed2=seed2, length=4)

    dct_blocks = apply_dct_to_blocks(blocks)
    flat_watermark = decorelate_pseudorandom_sequences(dct_blocks, pn0, pn1)
    watermark = reconstruct_watermark(flat_watermark)
    if watermark is not None:
        return watermark

    return None


def image_4_x_4_division(image) -> list:
    blocks = []
    m, n = image.shape
    for i in range(3, n, 4):
        for j in range(3, m, 4):
            blocks.append(image[i - 4 + 1:i + 1, j - 4 + 1:j + 1])

    return blocks


def reshape_4_x_4_blocks_to_image(blocks, image_size):
    # how many blocks in a line or column
    n = image_size // 4
    reshaped_image = np.zeros((image_size, image_size))

    for i in range(0, n):
        for j in range(0, n):
            reshaped_image[i * 4:i * 4 + 4, j * 4: j * 4 + 4] = blocks[i * n + j]

    return reshaped_image


def apply_dct_to_blocks(blocks) -> list:
    dct_blocks = []
    for i in range(0, len(blocks)):
        dct_blocks.append(cv2.dct(blocks[i].astype('float32')))
    return dct_blocks


def apply_idct_to_blocks(dct_blocks) -> list:
    idct_blocks = []
    for i in range(0, len(dct_blocks)):
        idct_blocks.append(cv2.idct(dct_blocks[i].astype('float32')))
    return idct_blocks


def to_binary(image):
    binary = np.zeros(image.shape)
    (m, n) = image.shape
    for i in range(0, n):
        for j in range(0, n):
            if image[i][j] > 126:
                binary[i][j] = 1
    return binary


def generate_pseudorandom_sequences(seed1, seed2, length):
    pn0 = []
    pn1 = []
    for i in range(0, length):
        random.seed(seed1 + i)
        pn0.append(random.random())
        random.seed(seed2 + i)
        pn1.append(random.random())

    return pn0, pn1


def embed_pseudorandom_sequences(dct_blocks, pn0, pn1, watermark, alpha):
    n, _ = watermark.shape
    if n * n != len(dct_blocks):
        print('watermark size doesn''t fit to the image size')
        return None

    for i in range(0, n):
        for j in range(0, n):
            if watermark[i, j] == 0:
                dct_blocks[i * n + j] = embed_midband_coefficient(dct_blocks[i * n + j], pn0, alpha)
            else:
                dct_blocks[i * n + j] = embed_midband_coefficient(dct_blocks[i * n + j], pn1, alpha)
    return dct_blocks


def decorelate_pseudorandom_sequences(dct_blocks, pn0, pn1):
    n = len(dct_blocks)
    flat_watermark = []
    for i in range(0, n):
        flat_watermark.append(extract_midband_coefficient(dct_blocks[i], pn0, pn1))

    return flat_watermark


def embed_midband_coefficient(dct_block, pn, alpha):
    mid_matrix = dct_block[1:3, 1:3]
    m, n = mid_matrix.shape
    for i in range(0, n):
        for j in range(0, n):
            mid_matrix[i, j] += alpha * pn[i * n + j]
    dct_block[1:3, 1:3] = mid_matrix

    return dct_block


def extract_midband_coefficient(dct_block, pn_0, pn_1):
    mid_matrix = dct_block[1:3, 1:3]
    flat_mid_matrix = mid_matrix.flatten()
    cor_0 = np.corrcoef(flat_mid_matrix, pn_0)
    cor_1 = np.corrcoef(flat_mid_matrix, pn_1)
    cor_0 = np.sum(abs(cor_0))
    cor_1 = np.sum(abs(cor_1))

    if cor_0 > cor_1:
        return 0
    return 1


def reshape_4x4_blocks_to_image(blocks, image_size):
    # how many blocks in a line or column
    n = image_size // 4
    reshaped_image = np.zeros((image_size, image_size))

    for i in range(0, n):
        for j in range(0, n):
            reshaped_image[i * 4:i * 4 + 4, j * 4: j * 4 + 4] = blocks[i * n + j]

    return reshaped_image


def reconstruct_watermark(flat_watermark):
    rows = np.sqrt(len(flat_watermark))
    try:
        rows = rows.astype(int)
    except AttributeError:
        print('flat watermark was not of form n*n')
        return None
    watermark = np.zeros([rows, rows])
    for i in range(0, rows):
        for j in range(0, rows):
            watermark[i, j] = flat_watermark[i * rows + j]
    return watermark
