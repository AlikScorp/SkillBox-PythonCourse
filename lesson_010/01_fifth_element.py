# -*- coding: utf-8 -*-

# Умножить константу BRUCE_WILLIS на пятый элемент строки, введенный пользователем

BRUCE_WILLIS = 42

input_data = input('Если хочешь что-нибудь сделать, сделай это сам: ')

try:
    leeloo = int(input_data[4])
    result = BRUCE_WILLIS * leeloo
except ValueError as exc:
    print(f'В веденной строке под индексом четыре не число. Ошибка - "{exc}" с параметрами {exc.args}!')
except IndexError as exc:
    print(f'В веденной строке нет индекса с номером 4. Ошибка - "{exc}" с параметрами {exc.args}!')
except Exception as exc:
    print(f'Возникла неизвестная ошибка {exc} с параметрами {exc.args}!')
else:
    print(f"- Leeloo Dallas! Multi-pass № {result}!")

# Ообернуть код и обработать исключительные ситуации для произвольных входных параметров
# - ValueError - невозможно преобразовать к числу
# - IndexError - выход за границы списка
# - остальные исключения
# для каждого типа исключений написать на консоль соотв. сообщение

# зачет!
