# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел


def get_prime_numbers(n):
    prime_numbers = []
    for num in range(2, n + 1):
        for prime in prime_numbers:
            if num % prime == 0:
                break
        else:
            prime_numbers.append(num)
    return prime_numbers


# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:

    def __init__(self, n):
        self.item = 2
        self.n = n
        self.prime_numbers = []

    def __iter__(self):
        self.item = 2
        self.prime_numbers = []
        return self

    def __next__(self):

        for item in range(self.item, self.n + 1):
            for prime in self.prime_numbers:
                if item % prime == 0:
                    break
            else:
                self.prime_numbers.append(item)
                self.item = item
                return self.item

        raise StopIteration


# prime_number_iterator = PrimeNumbers(n=10000)
# for number in prime_number_iterator:
#     print(number)


# после подтверждения части 1 преподователем, можно делать
# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


def prime_numbers_generator(n: int, func=None):
    """
        Функция-генератор, возвращает простые числа в отрезке от 2 до n.
    :param n: Максимальная граница для поиска
    :param func: Дополнительно принемаемая функция-фильтр для отбора
    :return:
    """
    prime_numbers = []
    for num in range(2, n + 1):
        for prime in prime_numbers:
            if num % prime == 0:
                break
        else:
            prime_numbers.append(num)
            if func is None:
                yield num
            else:
                if func(num):
                    yield num
                else:
                    continue


print('Prime numbers by generator:', '[', sep='\n', end='')
for number in prime_numbers_generator(n=10000):
    print(number, end=', ')
print(']')


# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.


# Не уврен в правильности релизации задания, возможно что я неправильно его понял.
# Может быть фильтрацию нужно заложить в сам генератор или итератор?

def is_lucky_number(n: int) -> bool:
    """
        Функция проверяет полученное число на "счастливость" - сумма первых цифр равна сумме последних.
        Если число имеет нечетное число цифр, то для вычисления берется равное количество символов с начала и конца.
    :param n: Целое число
    :return: True если переданное чило счастливое и False в противном случае
    """
    str_number = str(n)
    length = len(str_number)
    half = length // 2

    if length == 1:
        return False

    if length % 2 == 0:
        return is_parts_equal(str_number[:half], str_number[half:])
    else:
        return is_parts_equal(str_number[:half], str_number[half + 1:])


def is_parts_equal(first: str, second: str) -> bool:
    """
        Функция сумирует цифры в полученных переменных и проверяет полученные суммы на равенство.
    :param first: Первое число
    :param second: Второе число
    :return: True если суммы цифр в first и second равны и False в противном случае
    """

    return sum(map(int, first)) == sum(map(int, second))


def is_palindrome_number(n: int) -> bool:
    """
        Функция проверяем является ли принимаемое число палиндромом
    :param n: Проверяемое число
    :return: True если число является палинромом False в противном случае
    """
    str_number = str(n)

    return str_number == str_number[-1::-1]


def is_sophie_germain_number(n: int) -> bool:
    """
        Функция проверяет является ли принимаемое простое число простым числом Софи Жермен.
        Простое число n является простым числом Софи Жермен если 2n+1 также простое число.
    :param n: Простое число
    :return: True в случае если n является простым числом Софи Жермен и False в противном случае.
    """

    num = 2*n + 1

    if num < 2:
        return False
    result = True

    for i in range(2, int(num/2)):
        if num % i == 0:
            result = False
            break
    return result


lucky_numbers = list(filter(is_lucky_number, prime_numbers_generator(n=10000)))
print("List of prime and lucky numbers:", lucky_numbers, sep='\n')
#
# palindrome_numbers = list(filter(is_palindrome_number, prime_numbers_generator(n=10000)))
# print("List of prime and palindrome numbers:", palindrome_numbers, sep='\n')
#
prime_numbers_10000 = list(prime_numbers_generator(n=10000))
sophie_germain_numbers = list(filter(is_sophie_germain_number, prime_numbers_generator(n=10000)))
print("List of prime and Sophie Germain numbers:", sophie_germain_numbers, sep='\n')

#  Накладываем дополнительный фильтр на уже отфильтрованный список
# sophie_germain_palindrome_numbers = list(filter(is_sophie_germain_number, palindrome_numbers))
# print("List of prime and Sophie Germain palindrome numbers:", sophie_germain_palindrome_numbers, sep='\n')

#  Искать простые "счастливые" палиндромные числа помоему нет смысла - любой полиндром будет "счастливым" числом
#  Палиндром нечётной длины не будет счастливым.

print('Prime numbers by generator with internal filtration:', '[', sep='\n', end='')
for number in prime_numbers_generator(n=10000, func=is_sophie_germain_number):
    print(number, end=', ')
print(']')
