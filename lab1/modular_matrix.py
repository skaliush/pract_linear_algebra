import numpy as np


def mod_inv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"Обратного элемента для {a} по модулю {m} не существует.")
    else:
        return x % m


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x


def matrix_mod_inv(A, m):
    det = int(np.round(np.linalg.det(A)))
    det_inv = mod_inv(det % m, m)

    # Матрица алгебраических дополнений и транспонирование (присоединённая матрица)
    adjugate_matrix = np.round(det * np.linalg.inv(A)).astype(int) % m

    # Вычисление обратной матрицы по модулю
    inv_matrix = (det_inv * adjugate_matrix) % m
    return inv_matrix
