# -*- coding: utf-8 -*-

from lesson_005 import room_1 as r1
from lesson_005 import room_2 as r2

# Вывести на консоль жителей комнат (модули room_1 и room_2)
# Формат: В комнате room_1 живут: ...

# TODO здесь ваш код
print('В комнате room_1 живут:')
for i, person in enumerate(r1.folks):
    print('\t', i + 1, ') ', person, sep='')

print('В комнате room_2 живут:')
for i, person in enumerate(r2.folks):
    print('\t', i + 1, ') ', person, sep='')
