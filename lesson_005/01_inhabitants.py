# -*- coding: utf-8 -*-

from lesson_005 import room_1 as r1
from lesson_005 import room_2 as r2

# Вывести на консоль жителей комнат (модули room_1 и room_2)
# Формат: В комнате room_1 живут: ...

print('В комнате room_1 живут:')
for i, person in enumerate(r1.folks, start=1):
    print('\t', i, ') ', person, sep='')

print('В комнате room_2 живут:')
for i, person in enumerate(r2.folks, start=1):
    print('\t', i, ') ', person, sep='')
