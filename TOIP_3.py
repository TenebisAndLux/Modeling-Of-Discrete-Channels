import numpy as np


def generate_lambda_by_normal(param, z):
    """
    Генерирует лямбда по нормальному распределению.

    :param param: список с параметрами распределения [минимальное значение, максимальное значение]
    :param z: список случайных чисел
    :return: список сгенерированных лямбда
    """
    return [param[0] + (param[1] - param[0]) * el for el in z]


n = 15
z = np.random.rand(n)
l = generate_lambda_by_normal([0, 10], z)

e = np.array([i for el in [[0] * int(e) + [1] for e in l] for i in el])


def get_interval_by_epsilon(e):
    """
    Разделяет последовательность на интервалы с ошибками и без ошибок.

    :param e: последовательность ошибок
    :return: два списка - интервалы ошибок и интервалы без ошибок
    """
    error_interval = []
    packate = []
    not_error_interval = []
    inteval = []
    for i in range(len(e)):
        if e[i] == 0:
            packate.append(e[i])
            if len(inteval) != 0:
                error_interval.append(len(inteval))
                inteval = []
        else:
            inteval.append(e[i])
            if len(packate) != 0:
                not_error_interval.append(len(packate))
                packate = []
        if i == len(e) - 1:
            if len(inteval) != 0:
                error_interval.append(len(inteval))
                inteval = []
            if len(packate) != 0:
                not_error_interval.append(len(packate))
                packate = []
    return error_interval, not_error_interval


error_interval, not_error_interval = get_interval_by_epsilon(e)

m = 2


def get_error_sequence_by_block(e, m):
    """
    Разделяет последовательность на блочные интервалы.

    :param e: последовательность ошибок
    :param m: размер блока
    :return: список блочных интервалов
    """
    result = []
    for i in range(0, len(e), m):
        result.append(e[i:i + m])
    return result


e_k = get_error_sequence_by_block(e, m)


def get_interval_by_error_sequence(e):
    """
    Получает интервалы по последовательности ошибок.

    :param e: последовательность ошибок
    :return: список интервалов ошибок
    """
    result = []
    count = 0
    for i in range(len(e)):
        if e[i] == 0:
            count += 1
        else:
            result.append(count)
            count = 0
    return result


print("Интервальное представление: ", get_interval_by_error_sequence(e))


def get_error_coefficient(e):
    """
    Возвращает коэффициент ошибок.
    :param e: последовательность ошибок
    :return: коэффициент ошибок
    """
    return sum(e) / len(e)


print("Коэффициент ошибок: ", get_error_coefficient(e))


def get_grouping_coefficient(e_k):
    """
    Возвращает коэффициент группирования.
    :param e_k: последовательность ошибок
    :return: коэффициент группирования и количество ненулевых групп
    """
    kl = 0
    m = len(e_k[0])
    k = sum([sum(el) for el in e_k])
    for el in e_k:
        if sum(el) != 0:
            kl = kl + 1
    return (np.log(k) - np.log(kl)) / np.log(m), kl


g_k = get_grouping_coefficient(e_k)[0]
kl = get_grouping_coefficient(e_k)[1]
print("Коэффициент группирования: ", g_k)


def get_error_coefficient_by_block(kl, e_k):
    """
    Возвращает коэффициент ошибок по блокам.
    :param kl: количество ненулевых групп
    :param e_k: последовательность ошибок
    :return: коэффициент ошибок по блокам
    """
    return kl / (len(e_k))


print("Коэффициент ошибок по блокам: ", get_error_coefficient_by_block(kl, e_k))


def get_interval_by_error_sequence_block(e_k):
    """
    Получает интервалы по последовательности ошибок в блоках.
    :param e_k: последовательность ошибок
    :return: список интервалов ошибок
    """
    result = []
    count = 0
    for i in range(len(e_k)):
        if sum(e_k[i]) == 0:
            count += 1
        else:
            result.append(count)
            count = 0
    return result


print("Интервальное представление для e_k: ", get_interval_by_error_sequence_block(e_k))


def generate_error_by_markov(p_00, p_11, n):
    """
    Генерирует последовательность ошибок по модели Маркова.
        :param p_00: вероятность перехода из состояния 0 в состояние 0
        :param p_11: вероятность перехода из состояния 1 в состояние 1
        :param n: количество элементов в последовательности
        :return: сгенерированная последовательность ошибок
    """
    result = []
    p_01 = 1 - p_00
    for i in range(n):
        if i == 0:
            if np.random.rand() < p_00:
                result.append(0)
            else:
                result.append(1)
        else:
            if result[i - 1] == 0:
                if np.random.rand() < p_01:
                    result.append(1)
                else:
                    result.append(0)
            else:
                if np.random.rand() < p_11:
                    result.append(1)
                else:
                    result.append(0)
    return result


# Генерация последовательности ошибок по модели Маркова с заданными параметрами
p_00 = 0.9
p_11 = 0.2
n = 300
e = generate_error_by_markov(p_00, p_11, n)

# Вывод сгенерированной последовательности ошибок
print("Последовательность ошибок: ", e)

# Получение последовательности ошибок в блоках (пакетах)
e_k = get_error_sequence_by_block(e, m)
print("Последовательность ошибок блочных(пакетных): ", e_k)

# Вычисление коэффициента ошибок
error_koefficient = get_error_coefficient(e)
print("Коэффициент ошибок: ", error_koefficient)

# Вычисление коэффициента группирования
g_k = get_grouping_coefficient(e_k)[0]
print("Коэффициент группирования: ", g_k)

# Вывод идеальных параметров второго уровня и оценка параметров второго уровня на основе полученных данных
print("Идеальные параметры второго уровня:", "\n", "p_00 = ", p_00, "\n", "p_11 = ", p_11, "\n", "p_01 = ", 1 - p_00,
      "\n", "p_10 = ", 1 - p_11)
p_11 = 2 - 2 ** (1 - g_k)
p_00 = (1 - (2 * m) ** (1 - g_k) * error_koefficient) / (1 - m ** (1 - g_k) * error_koefficient)
print("Оценка параметров второго уровня:", "\n", "p_00 = ", p_00, "\n", "p_11 = ", p_11, "\n", "p_01 = ", 1 - p_00,
      "\n", "p_10 = ", 1 - p_11)
