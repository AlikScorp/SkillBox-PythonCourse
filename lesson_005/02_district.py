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

# TODO Обращайте внимание на предупреждения среды разработки о нарушении стандарта PEP 8.
#  Попробуйте найти зеленую галочку справа над полосой прокрутки.
#  Если вместо нее, квадрат красного, желтого или серого цвета,
#  значит в файле есть недостатки оформления или ошибки.
#  Здесь вы переопределяете переменную people не использовав ее более раннюю копию.
# TODO Лучше длинные выражения заключать в скобки. Тогда их получается отформатировать
#  без использования обратного слэша.
people = dch1r1_folks + dch1r2_folks + dch2r1_folks + dch2r2_folks +\
         dsh1r1_folks + dsh1r2_folks + dsh2r1_folks + dsh2r2_folks
inhabitants = ', '.join(people)
print('На районе живут:', inhabitants)
