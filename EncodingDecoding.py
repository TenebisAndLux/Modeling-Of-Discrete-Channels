import numpy as np
import random
import queue
from sys import setrecursionlimit
import matplotlib.pyplot as plt


class Node:
    def __init__(self, fr, ky=-1, l=None, r=None, cod=''):
        self.freq = fr
        self.key = ky
        self.left = l
        self.right = r
        self.code = cod

    def __lt__(self, otr):
        return self.freq < otr.freq


setrecursionlimit(300000)

##step 1
J = np.random.rand(100000)
##step 2
## экспоненциальный lambda = 2
lamda = 2
##Случайная величина
xj = (-1 / lamda) * np.log(J)
##step 3
x_max = np.max(xj)
x_min = np.min(xj)
M = np.mean(xj)
D = np.var(xj)
std_dev = np.std(xj)

hist_digits, _ = np.histogram(xj, bins=10, range=(0, 2.5))
hist_alp, _ = np.histogram(xj, bins=33 * 2 + 26 * 2, range=(0, 2.5), density=True)
hist_unicode, _ = np.histogram(xj, bins=1000, range=(0, 1), density=True)

prob_unicode = hist_unicode / (np.sum(hist_unicode))
prob_d = hist_digits / (np.sum(hist_digits))
prob_a = hist_alp / (np.sum(hist_alp))

## словарь под цифры
arr_digits = [i for i in range(10)]
dict_digits = dict(zip(arr_digits, prob_d))
## словарь под буквы
arr_alp = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 122)] + [chr(i) for i in range(1040, 1104)]
dict_alp = dict(zip(arr_alp, prob_a))
## словарь под unicode
arr_unicode = [chr(i) for i in range(33, 1034)]
dict_unicode = dict(zip(arr_unicode, prob_unicode))

print(dict_digits)
print(" ")
print(dict_alp)
print(" ")
print(dict_unicode)
print(" ")


## алгоритм кодирования Хафмана рекурсивно возвращает dict
def huffman(dict):
    list = []
    for i in dict:
        list.append(Node(dict[i], i))
    list.sort(key=lambda i: i.freq)
    while len(list) > 1:
        list.sort(key=lambda i: i.freq)
        node = Node(list[0].freq + list[1].freq, l=list[0], r=list[1])
        list.pop(0)
        list.pop(0)
        list.append(node)
    codes = {}

    def _huffman(node, code=''):
        if node.key != -1:
            codes[node.key] = code
        else:
            _huffman(node.left, code + '0')
            _huffman(node.right, code + '1')

    _huffman(list[0])
    return codes


## алгоритм Шеннона-Фано dict
def _shannon_fano(list, code=''):
    if len(list) == 1:
        list[0].code = code
    else:
        mid = len(list) // 2
        for i in range(mid):
            list[i].code = code + '0'
        for i in range(mid, len(list)):
            list[i].code = code + '1'
        _shannon_fano(list[:mid], code + '0')
        _shannon_fano(list[mid:], code + '1')


def shenon_fano(dict):
    list = []
    for i in dict:
        list.append(Node(dict[i], i))
    _shannon_fano(list)
    codes = {}
    for i in list:
        codes[i.key] = i.code
    return codes


##алгоритм кодирования
def algorytmTypeProcessing(encoded, message, dict_alp, dict_digits, dict_unicode):
    for i in message:
        if i in dict_digits:
            encoded.append(dict_digits[i])
        elif i in dict_alp:
            encoded.append(dict_alp[i])
        elif i in dict_unicode:
            encoded.append(dict_unicode[i])
    return encoded


##кодирование  сообщения
def encode(message, dict_alp, dict_digits, dict_unicode):
    encoded = []
    encoded = algorytmTypeProcessing(encoded, message, dict_alp, dict_digits, dict_unicode)

    return encoded

## кодирование сообщения единой строкой -> накапливаем переменную, если накопленная переменная есть в словаре, то
## декодируем ее и добавляем в строку


##поиск ключа по значению
def find_key(dict, value):
    for key, v in dict.items():
        if v == value:
            return key


## декодирование сообщения
def decode(encoded, dict_alp, dict_digits, dict_unicode):
    decoded = []
    for i in encoded:
        if i in dict_digits.values():
            decoded.append(find_key(dict_digits, i))
        elif i in dict_alp.values():
            decoded.append(find_key(dict_alp, i))
        elif i in dict_unicode.values():
            decoded.append(find_key(dict_unicode, i))
    return decoded

## длина кодовой комбинации
def code_length(dict):
    length = 0
    for i in dict:
        length += len(dict[i])
    return length

## длина словаря
def dict_length(dict):
    return dict.__len__()

## Оценка значения средней длительности кодовых комбинаций
def average_length(dict):
    return (1 / dict_length(dict)) * code_length(dict)


shenon_d = shenon_fano(dict_digits)
shenon_a = shenon_fano(dict_alp)
shenon_u = shenon_fano(dict_unicode)

huffman_d = huffman(dict_digits)
huffman_a = huffman(dict_alp)
huffman_u = huffman(dict_unicode)

print("")
print("--Алгоритм Шеннона-Фано--")
print("")

print("Алгоритм Шеннона-Фано для цифр: ")
print(shenon_d)

print("Алгоритм Шеннона-Фано для букв: ")
print(shenon_a)

print("Алгоритм Шеннона-Фано для unicode: ")
print(shenon_u)

print("")
print("--Алгоритм Хаффмана--")
print("")

print("Алгоритм Хаффмана для цифр: ")
print(huffman_d)

print("Алгоритм Хаффмана для букв: ")
print(huffman_a)

print("Алгоритм Хаффмана для unicode: ")
print(huffman_u)

print("")
print("--Кодирование сообщения Хаффманом--")
print("")

print("8800553535")
print(encode("8800553535", huffman_a, huffman_d, huffman_u))
print("I have many favourite artists. Among them are writers, painters and musicians.")
print(encode("I have many favourite artists. Among them are writers, painters and musicians.", huffman_a,
             huffman_d, huffman_u))
print("I have many favourite artists. Among them are writers, painters and musicians.")
print(encode(
    "I have many favourite artists. Among them are writers, painters and musicians.", huffman_a, huffman_d,
    huffman_u))

print("")
print("--Кодирование сообщения Шенноном-Фано--")
print("")

print("88800553535")
print(encode("88800553535", shenon_a, shenon_d, shenon_u))
print("I have many favourite artists. Among them are writers, painters and musicians.")
print(encode("I have many favourite artists. Among them are writers, painters and musicians.", shenon_a,
             shenon_d, shenon_u))
print("I have many favourite artists. Among them are writers, painters and musicians.")
print(encode("I have many favourite artists. Among them are writers, painters and musicians.", shenon_a, shenon_d,
             shenon_u))

print("")
print("--Декодер тесты--")
print("")

test = encode("I have many favourite artists. Among them are writers, painters and musicians.", huffman_a, huffman_d,
              huffman_u)
print(decode(test, huffman_a, huffman_d, huffman_u))

print("")
print("--Оценка значения средней длительности кодовых комбинаций--")
print("")

print(average_length(shenon_u))