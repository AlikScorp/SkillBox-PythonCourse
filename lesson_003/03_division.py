# -*- coding: utf-8 -*-

# (цикл while)

# даны целые положительные числа a и b (a > b)
# Определить результат целочисленного деления a на b, с помощью цикла while,
# __НЕ__ используя стандартную операцию целочисленного деления (// и %)
# Формат вывода:
#   Целочисленное деление ХХХ на YYY дает ZZZ

a, b = 179, 37

string = 'Целочисленное деление ' + str(a) + ' на ' + str(b)
i = 0
while a >= b:
    a -= b
    i += 1

print(string, 'дает', i)

# зачет!
