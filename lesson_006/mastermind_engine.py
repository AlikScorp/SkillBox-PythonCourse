from random import randint

number = []


def generate_number(quantity):
    for i in range(quantity):
            start = 0 if i != 0 else 1
            # TODO Не самый оптимальный способ генерации числа.
            #  В библиотеке random есть более подходящие функции.
            #  Например shuffle или sample. Можно получить сразу всю
            #  случайную последовательность одной командой.
            #  Если хотите избегать 0 на первой позиции,
            #  то генерировать последовательлность можно
            #  пока не получим последовательность начинающуюся не с 0.
            while True:
                figure = randint(start, 9)
                if figure not in number:
                    number.append(figure)
                    break


def check_number(num):
    result = {'bulls': 0, 'cows': 0}
    for i in range(len(num)):
        if int(num[i]) in number:
            if i == number.index(int(num[i])):
                result['bulls'] += 1
            else:
                result['cows'] += 1
    return result


if __name__ == "__main__":
    generate_number(4)
    print(number)
    print(check_number('2345'))
