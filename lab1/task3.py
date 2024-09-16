import random
import numpy as np

alphabet = {
    'А': '00000', 'Б': '00001', 'В': '00010', 'Г': '00011', 'Д': '00100',
    'Е': '00101', 'Ж': '00110', 'З': '00111', 'И': '01000', 'Й': '01001',
    'К': '01010', 'Л': '01011', 'М': '01100', 'Н': '01101', 'О': '01110',
    'П': '01111', 'Р': '10000', 'С': '10001', 'Т': '10010', 'У': '10011',
    'Ф': '10100', 'Х': '10101', 'Ц': '10110', 'Ч': '10111', 'Ш': '11000',
    'Щ': '11001', 'Ъ': '11010', 'Ы': '11011', 'Ь': '11100', 'Э': '11101',
    'Ю': '11110', 'Я': '11111',
}

inverted_alphabet = {value: key for key, value in alphabet.items()}

alpha_len = len(alphabet)


def letter_to_code(letter):
    return alphabet[letter]


def code_to_letter(code):
    return inverted_alphabet[code]


def replace_char_by_index(text, index, replacement):
    return f'{text[:index]}{replacement}{text[index + 1:]}'


def translate_text_to_bits(text):
    sequence = ''
    for l in text:
        sequence += letter_to_code(l)
    return sequence


def beat_the_bit(sequence, index):
    random_bit = bool(int(sequence[index]))
    return replace_char_by_index(sequence, index, str(int(not random_bit)))


def translate_bits_to_text(bits):
    i = 1
    letter_code = ''
    text = ''
    for b in bits:
        letter_code += b
        if i % 5 == 0:
            text += code_to_letter(letter_code)
            letter_code = ''
        i += 1
    return text


def encode_hamming74(msg):
    r = 3
    n = 2 ** r - 1
    k = n - r

    if len(msg) % k != 0:
        raise ValueError('incorrect r')

    i = 1
    block = []
    result = ''

    G = [
        [1, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 0, 0, 1],
    ]

    for b in msg:
        block.append(int(b))
        if i % k == 0:
            encoded_block = np.dot(block, G) % 2
            total_parity_bit = encoded_block.sum() % 2
            encoded_block = np.append(encoded_block, total_parity_bit)
            encoded_string = ''.join(encoded_block.astype(str))
            result += encoded_string
            block = []
        i += 1
    return result


def decode_hamming74(code):
    r = 3
    n = 2 ** r - 1
    k = n - r

    H = [
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1],
    ]

    i = 1
    block = []
    result = ''
    for b in code:
        block.append(int(b))
        if i % (n + 1) == 0:
            # checking & fixing possible errors
            total_parity = not bool(int(sum(block) % 2))
            del block[-1]  # deleting the total parity bit

            error_syndrome = np.dot(block, H) % 2
            is_error_exist = sum(error_syndrome) > 0
            if is_error_exist:
                if total_parity:
                    print('Обнаружено четное количество ошибок в блоке: восстановить блок невозможно')
                else:
                    print('Обнаружено нечетное количество ошибок в блоке: попытка восстановить ошибку')
                    broken_index = int(''.join(map(str, error_syndrome[::-1])), 2) - 1
                    # print('broken_index:', broken_index)
                    block[broken_index] = int(not bool(block[broken_index]))
            else:
                if total_parity:
                    print('Ошибок в блоке не обнаружено')
                else:
                    print('Ошибка обнаружена в бите общей четности')

            # extracting the content bits
            for power in range(r - 1, -1, -1):
                del block[2 ** power - 1]  # deleting check bits
            result += ''.join(map(str, block))
            block = []
        i += 1
    return result


text_msg = 'МИРА'
# print('text_msg:   ', text_msg)

msg = translate_text_to_bits(text_msg)
# print('msg:        ', msg)
encoded_msg = encode_hamming74(msg)
print('encoded_msg:', encoded_msg)

random_index = random.randint(0, len(encoded_msg) - 1)
broken_msg = beat_the_bit(encoded_msg, random_index)
print('broken_msg: ', broken_msg, '// index:', random_index, '(mod 8) =', random_index % 8)

# random_index += 1
# broken_msg = beat_the_bit(broken_msg, random_index)
# print('broken_msg: ', broken_msg, '// index:', random_index, '(mod 8) =', random_index % 8)

decoded_msg = decode_hamming74(broken_msg)

print('msg:        ', msg)
print('decoded_msg:', decoded_msg)
decoded_text_msg = translate_bits_to_text(decoded_msg)
print('result:     ', decoded_text_msg)
