#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть строка с перечислением фильмов

my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'

# Выведите на консоль с помощью индексации строки, последовательно:
#   первый фильм
#   последний
#   второй
#   второй с конца

# Переопределять my_favorite_movies и использовать .split() нельзя.
# Запятая не должна выводиться.

print("Первый фильм:", my_favorite_movies[:10])
print("Последний фильм:", my_favorite_movies[-15:])
print("Второй фильм:", my_favorite_movies[12:25])
print("Второй с конца фильм:", my_favorite_movies[-22:-17])
