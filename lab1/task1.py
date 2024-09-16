import random

import numpy as np
import modular_matrix as mm

alphabet = {
    'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4,
    'е': 5, 'ё': 6, 'ж': 7, 'з': 8, 'и': 9,
    'й': 10, 'к': 11, 'л': 12, 'м': 13, 'н': 14,
    'о': 15, 'п': 16, 'р': 17, 'с': 18, 'т': 19,
    'у': 20, 'ф': 21, 'х': 22, 'ц': 23, 'ч': 24,
    'ш': 25, 'щ': 26, 'ъ': 27, 'ы': 28, 'ь': 29,
    'э': 30, 'ю': 31, 'я': 32, ' ': 33, ',': 34,
    '.': 35, '?': 36
}

inverted_alphabet = {value: key for key, value in alphabet.items()}

alpha_len = len(alphabet)


def letter_to_code(letter):
    return alphabet[letter]


def code_to_letter(code):
    return inverted_alphabet[code]


### Encoding

def encode_msg(msg, key, n):
    while len(msg) % n != 0:
        msg += ' '

    i = 1
    block = []
    result = ''
    for l in msg:
        code = letter_to_code(l)
        block.append(code)
        if i % n == 0:
            encoded_vector = key.dot(block) % alpha_len
            for coord in encoded_vector:
                result += code_to_letter(coord)
            block = []
        i += 1
    return result


key2 = np.array([
    [1, 2],
    [3, 4],
])
key3 = np.array([
    [6, 24, 1],
    [13, 16, 10],
    [20, 17, 15],
])
key4 = np.array([
    [11, 2, 3, 4],
    [0, 6, 7, 8],
    [9, 10, 7, 12],
    [13, 3, 1, 16],
])

msg = 'воля и разум'
# msg = input()

encoded_msg2 = encode_msg(msg, key2, 2)
print(encoded_msg2)
encoded_msg3 = encode_msg(msg, key3, 3)
print(encoded_msg3)
encoded_msg4 = encode_msg(msg, key4, 4)
print(encoded_msg4)


### Decoding

def decode_msg(msg, key, n):
    if len(msg) % n != 0:
        raise ValueError('incorrect code')
    inverted_key = mm.matrix_mod_inv(key, alpha_len)

    i = 1
    block = []
    result = ''
    for l in msg:
        code = letter_to_code(l)
        block.append(code)
        if i % n == 0:
            original_vector = inverted_key.dot(block) % alpha_len
            for coord in original_vector:
                result += code_to_letter(coord)
            block = []
        i += 1
    return result


def replace_char_by_index(text, index, replacement):
    return f'{text[:index]}{replacement}{text[index + 1:]}'


print()

encoded_msg4 = replace_char_by_index(encoded_msg4, random.randint(0, len(encoded_msg2) - 1), '?')

decoded_msg = decode_msg(encoded_msg2, key2, 2)
print(decoded_msg)
decoded_msg = decode_msg(encoded_msg3, key3, 3)
print(decoded_msg)
decoded_msg = decode_msg(encoded_msg4, key4, 4)
print(decoded_msg)
