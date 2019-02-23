# -*- coding: utf-8 -*-

from lesson_005.district.central_street.house1.room1 import folks as dch1r1_folks
from lesson_005.district.central_street.house1.room2 import folks as dch1r2_folks
from lesson_005.district.central_street.house2.room1 import folks as dch2r1_folks
from lesson_005.district.central_street.house2.room2 import folks as dch2r2_folks
from lesson_005.district.soviet_street.house1.room1 import folks as dsh1r1_folks
from lesson_005.district.soviet_street.house1.room2 import folks as dsh1r2_folks
from lesson_005.district.soviet_street.house2.room1 import folks as dsh2r1_folks
from lesson_005.district.soviet_street.house2.room2 import folks as dsh2r2_folks

# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join

people = []

people += dch1r1_folks
people += dch1r2_folks
people += dch2r1_folks
people += dch2r2_folks
people += dsh1r1_folks
people += dsh1r2_folks
people += dsh2r1_folks
people += dsh2r2_folks
# TODO Вместо добавления каждой комнаты по отдельности можно задать
#  people как сумму *_folks одной операцией. Т. е. вмемто
#  my_list = []
#  my_list += [1, 2]
#  my_list += [3, 4]
#  сделать
#  my_list = [1, 2] + [3, 4]
inhabitants = ', '.join(people)
print('На районе живут:', inhabitants)
