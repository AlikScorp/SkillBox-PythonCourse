# -*- coding: utf-8 -*-

# (if/elif/else)

# По номеру месяца вывести кол-во дней в нем (без указания названия месяца, в феврале 28 дней)
# Результат проверки вывести на консоль
# Если номер месяца некорректен - сообщить об этом

# Номер месяца получать от пользователя следующим образом
user_input = input("Введите, пожалуйста, номер месяца: ")
month = int(user_input)
print('Вы ввели', month)

months = {'1': 31, '2': 28, '3': 31, '4': 30, '5': 31, '6': 30,
          '7': 31, '8': 31, '9': 30, '10': 31, '11': 30, '12': 31}

if str(month) in months:
    print('Количество дней в этом месяце равно', months[str(month)])
else:
    print('Месяца с номером', month, 'не существует')

# TODO Вместо цикла, вы можете использовать словарь
#  или несколько списков (для номеров месяцев с одинаковым количеством дней.)
#  Долго ломал голову как сделать с несколькими списками - так и не придумал! :-(
