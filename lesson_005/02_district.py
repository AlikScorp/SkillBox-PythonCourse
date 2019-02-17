# -*- coding: utf-8 -*-
from lesson_005.district.central_street.house1 import room1 as dch1r1, room2 as dch1r2
from lesson_005.district.central_street.house2 import room1 as dch2r1, room2 as dch2r2
from lesson_005.district.soviet_street.house1 import room1 as dsh1r1, room2 as dsh1r2
from lesson_005.district.soviet_street.house2 import room1 as dsh2r1, room2 as dsh2r2

# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join


people = []

people.extend(dch1r1.folks)
people.extend(dch1r2.folks)
people.extend(dch2r1.folks)
people.extend(dch2r2.folks)
people.extend(dsh1r1.folks)
people.extend(dsh1r2.folks)
people.extend(dsh2r1.folks)
people.extend(dsh2r2.folks)

inhabitants = ', '.join(people)
print('На районе живут:', inhabitants)
