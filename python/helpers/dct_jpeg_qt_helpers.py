import numpy as np
import cv2
from skimage import measure

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


def reverse_scramble_pixels(x, y, n):
    current_position = np.array([[x], [y]])
    const_window = np.array([[2, -1], [-1, 1]])

    return np.matmul(const_window, current_position) % n


def embed_watermark(watermark, image, key):
    scrambled_watermark = arnold_transform(watermark, key)
    blocks = image_8_x_8_division(image)
    (m, n) = image.shape
    k = []
    dct_blocks = []
    idct_blocks = []
    E = []
    watermark_bits = scrambled_watermark.flatten()
    if len(watermark_bits) != len(blocks):
        print('bits of not equal size to blocks')
        return None

    for i in range(0, len(blocks)):
        E.append(measure.shannon_entropy(blocks[i]))

    for i in range(0, len(blocks)):
        k.append(get_adaptive_adjustment_coefficient(blocks[i], E))
        dct_blocks.append(cv2.dct(blocks[i].astype('float32')))

    for i in range(0, len(k)):
        k[i] = normalize_adaptive_adjustment_coefficient(k[i], k)

    # we now take C1 and C2 pair of coefficients
    # which has the same value in the quantization table
    i1, j1 = pairs[0][0]
    i2, j2 = pairs[0][1]
    for i in range(0, len(dct_blocks)):
        C1 = dct_blocks[i][i1][j1]
        C2 = dct_blocks[i][i2][j2]
        if watermark_bits[i] == 0:
            if C1 < C2:
                aux = C1
                C1 = C2
                C2 = aux
        elif watermark_bits[i] == 1:
            if C1 >= C2:
                aux = C1
                C1 = C2
                C2 = aux
        if C1 > C2:
            if C1 - C2 > k[i]:
                C1 = C1 + k[i] / 2
                C2 = C2 - k[i] / 2
        elif C2 - C1 < k[i]:
            C1 = C1 - k[i] / 2
            C2 = C2 + k[i] / 2
        dct_blocks[i][i1][j1] = C1
        dct_blocks[i][i2][j2] = C2

    for i in range(0, len(dct_blocks)):
        idct_blocks.append(cv2.idct(dct_blocks[i]))

    return reshape_8x8_blocks_to_image(idct_blocks, n)


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
    for i in range(0, key-1):
        result = arnold_step(result)
    return result


def image_8_x_8_division(image) -> list:
    blocks = []
    m, n = image.shape
    for i in range(7, n, 8):
        for j in range(7, m, 8):
            blocks.append(image[i - 8 + 1:i + 1, j - 8 + 1:j + 1])

    return blocks


def get_masking_factor(block):
    beta = get_beta(block)
    ave = np.average(block)
    w = webber_ratio
    if ave < I1:
        w = ((beta - webber_ratio) * pow((ave - I1), 2)) / (I2 * I2) + webber_ratio
    if ave >= I2:
        w = ((beta - webber_ratio) * pow((ave - I2), 2)) / pow((255 - I2), 2) + webber_ratio
    return w


def get_entropy(block, E):
    e = measure.shannon_entropy(block)
    result = ((b - a) * (e - np.amin(E))) / (np.amax(E) - np.amin(E)) + a
    return result


def get_adaptive_adjustment_coefficient(block, E):
    w = get_masking_factor(block)
    e = get_entropy(block, E)
    k = w * e
    return k


def normalize_adaptive_adjustment_coefficient(k, K):
    return ((d - c) * (k - np.amin(K))) / (np.amax(K) - np.amin(K)) + c


def get_beta(image):
    return np.amax(image) - np.amin(image)


def to_binary(image):
    binary = np.zeros(image.shape)
    (m, n) = image.shape
    for i in range(0, n):
        for j in range(0, n):
            if image[i][j] > 126:
                binary[i][j] = 1
    return binary


def reshape_8x8_blocks_to_image(blocks, image_size):
    # how many blocks in a line or column
    n = image_size // 8
    reshaped_image = np.zeros((image_size, image_size))

    for i in range(0, n):
        for j in range(0, n):
            reshaped_image[i * 8:i * 8 + 8, j * 8: j * 8 + 8] = blocks[i * n + j]

    return reshaped_image


def extract_watermark(embeded_image, k):
    blocks = image_8_x_8_division(embeded_image)
    n = int(round(np.sqrt(len(blocks))))
    dct_blocks = []
    watermark_bits = []
    watermark_image = np.zeros((n, n))
    for i in range(0, len(blocks)):
        dct_blocks.append(cv2.dct(blocks[i].astype('float32')))

    i1, j1 = pairs[0][0]
    i2, j2 = pairs[0][1]
    for i in range(0, len(dct_blocks)):
        C1 = dct_blocks[i][i1][j1]
        C2 = dct_blocks[i][i2][j2]
        if C1 > C2:
            watermark_bits.append(0)
        elif C2 >= C1:
            watermark_bits.append(1)

    for i in range(0, n):
        for j in range(0, n):
            watermark_image[i, j] = watermark_bits[i * n + j]

    watermark = reverse_arnold(watermark_image, k)

    return watermark


def reverse_arnold(image, k):
    result = reverse_arnold_step(image)
    for i in range(0, k - 1):
        result = reverse_arnold_step(result)
    return result


def reverse_arnold_step(image):
    (m, n) = image.shape
    reverse_scrambled_image = np.zeros(image.shape)
    for x in range(0, n):
        for y in range(0, n):
            new_positions = reverse_scramble_pixels(x, y, n)
            reverse_scrambled_image[new_positions[0], new_positions[1]] = image[x, y]

    return reverse_scrambled_image



# def exec_embeding(image, watermark, key):
#     result = helper.embed_watermark(watermark, image, key)
#     cv2.imwrite('output.png', result)
#
#     return None
#
#
# def exec_extracting(image, key):
#     result = helper.extract_watermark(embeded_image=image, k=key)
#     result = result * 255
#
#     cv2.imwrite('extracted_wmk.png', result)
#     return None


# exec_embeding(original_image, watermark_binary, 7)
# exec_extracting(image=output_image, key=7)

# matrix = np.array([[1, 2], [3, 4]])
# arnold = helper.arnold_transform(matrix, 2)
# print(arnold)
# reverse = helper.reverse_arnold(arnold, 2)
# print(reverse)