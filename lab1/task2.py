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


### Hacking

def hack_the_cipher(encoded_msg, original_msg, n):
    n_squared = n ** 2
    if len(encoded_msg) < n_squared or len(original_msg) < n_squared:
        raise ValueError("can't solve")
    encoded_msg = encoded_msg[:n_squared]
    original_msg = original_msg[:n_squared]
    C = np.array(list(map(letter_to_code, encoded_msg)))
    C.shape = (n, n)
    C = C.transpose()
    P = np.array(list(map(letter_to_code, original_msg)))
    P.shape = (n, n)
    P = P.transpose()
    P_inv = mm.matrix_mod_inv(P, alpha_len)
    return C.dot(P_inv) % alpha_len


solved_key2 = hack_the_cipher('яьвпнчэтпяиб', 'воля и разум', 2)
print(solved_key2)
solved_key3 = hack_the_cipher('нпюю.дн.чц?ь', 'воля и разум', 3)
print(solved_key3)
# solved_key4 = hack_the_cipher('юцжгэнзфр ёэ', 'воля и разум', 4)
# print(solved_key4)
