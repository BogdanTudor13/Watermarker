import numpy as np
import cv2
import pywt
import random


def embed_watermark(key1, key2, key3, key4, image, watermark, alpha):
    binary_watermark = to_binary(watermark)
    scrambled_watermark = arnold_transform(binary_watermark, key1).flatten().tolist()
    (cA, (cH, cV, cD)) = pywt.dwt2(image, wavelet='haar')
    (m, n) = cV.shape
    blocks = image_8_x_8_division(cV)
    dct_blocks = apply_dct_to_blocks(blocks)
    altered_blocks = [0] * len(dct_blocks)
    I, J, pn = generate_random_positions_and_weights(seed1=key2, seed2=key3, seed3=key4, N=len(dct_blocks))
    for i in range(0, len(dct_blocks)):
        block = dct_blocks[i]
        block[I[i], J[i]] += (alpha * abs(pn[i])) * (-1) ** scrambled_watermark[i]
        altered_blocks[i] = block

    idct_blocks = []

    for block in altered_blocks:
        idct_blocks.append(cv2.idct(block))

    reconstructed_cv = reshape_8x8_blocks_to_image(idct_blocks, n)
    reconstructed_image = pywt.idwt2((cA, (cH, reconstructed_cv, cD)), wavelet='haar')
    return reconstructed_image


def extract_watermark(key1, key2, key3, original_image, image):
    (cA, (cH, cV, cD)) = pywt.dwt2(image, wavelet='haar')
    (o_cA, (o_cH, o_cV, o_cD)) = pywt.dwt2(original_image, wavelet='haar')
    blocks = image_8_x_8_division(cV)
    o_blocks = image_8_x_8_division(o_cV)
    dct_blocks = apply_dct_to_blocks(blocks)
    o_dct_blocks = apply_dct_to_blocks(o_blocks)

    I, J, pn = generate_random_positions_and_weights(seed1=key2, seed2=key3, seed3=0, N=len(dct_blocks))

    scrambled_watermark = []
    for i in range(0, len(dct_blocks)):
        block = dct_blocks[i]
        o_block = o_dct_blocks[i]
        if block[I[i], J[i]] - o_block[I[i], J[i]] > 0:
            scrambled_watermark.append(0)
        else:
            scrambled_watermark.append(1)
    n = int(round(np.sqrt(len(blocks))))
    watermark_image = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            watermark_image[i, j] = scrambled_watermark[i * n + j]
    watermark = reverse_arnold(watermark_image, key1)
    return watermark


def image_8_x_8_division(image) -> list:
    blocks = []
    m, n = image.shape
    for i in range(7, n, 8):
        for j in range(7, m, 8):
            blocks.append(image[i - 8 + 1:i + 1, j - 8 + 1:j + 1])

    return blocks


def reshape_8x8_blocks_to_image(blocks, image_size):
    # how many blocks in a line or column
    n = image_size // 8
    reshaped_image = np.zeros((image_size, image_size))

    for i in range(0, n):
        for j in range(0, n):
            reshaped_image[i * 8:i * 8 + 8, j * 8: j * 8 + 8] = blocks[i * n + j]

    return reshaped_image


def to_binary(image):
    binary = np.zeros(image.shape)
    (m, n) = image.shape
    for i in range(0, n):
        for j in range(0, n):
            if image[i][j] > 126:
                binary[i][j] = 1
    return binary


def apply_dct_to_blocks(blocks) -> list:
    dct_blocks = []
    for i in range(0, len(blocks)):
        dct_blocks.append(cv2.dct(blocks[i].astype('float32')))
    return dct_blocks


def arnold_step(image):
    (m, n) = image.shape
    scrambled_image = np.zeros(image.shape)
    for x in range(0, n):
        for y in range(0, n):
            new_positions = scramble_pixels(x, y, n)
            scrambled_image[new_positions[0], new_positions[1]] = image[x, y]

    return scrambled_image


def arnold_transform(image, key):
    result = arnold_step(image)
    for i in range(0, key - 1):
        result = arnold_step(result)
    return result


def scramble_pixels(x, y, n):
    current_position = np.array([[x], [y]])
    const_window = np.array([[1, 1], [1, 2]])

    return np.matmul(const_window, current_position) % n


def generate_random_positions_and_weights(seed1: int, seed2: int, seed3: int, N: int):
    random.seed(seed1)
    seq1 = [random.randrange(3, 8) for i in range(N)]
    random.seed(seed2)
    seq2 = [random.randrange(3, 8) for i in range(N)]
    np.random.seed(seed3)
    pn = np.random.normal(0, 1, size=(1, N))
    pn = pn.flatten()
    return seq1, seq2, pn


def reverse_scramble_pixels(x, y, n):
    current_position = np.array([[x], [y]])
    const_window = np.array([[2, -1], [-1, 1]])

    return np.matmul(const_window, current_position) % n


def reverse_arnold_step(image):
    (m, n) = image.shape
    reverse_scrambled_image = np.zeros(image.shape)
    for x in range(0, n):
        for y in range(0, n):
            new_positions = reverse_scramble_pixels(x, y, n)
            reverse_scrambled_image[new_positions[0], new_positions[1]] = image[x, y]

    return reverse_scrambled_image


def reverse_arnold(image, k):
    result = reverse_arnold_step(image)
    for i in range(0, k - 1):
        result = reverse_arnold_step(result)
    return result
