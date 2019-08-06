# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.


class NotNameError(Exception):
    pass


class NotEmailError(Exception):
    pass


def check_name(name: str) -> bool:
    """
        Функция проверяет переданный параметр на отсутствие каких-либо символов за исключением букв
        В случае нахождения не разрешенных символов вызывает кастомное исключение NotNameError
    :param name: Строковая переменная
    :return: В случае успеха возвращает True
    """
    if not name.isalpha():
        raise NotNameError('Username must be alphabetic')

    return True


def check_email(email: str) -> bool:
    """
        Функция проверяет переданный параметр на соответствие формату e-mail адреса
        В случае не соответствия вызывает кастомное исключение NotEmailError
    :param email: Строковый параметр
    :return: В случае успеха возвращает True
    """
    if '@' not in email and '.' not in email:
        raise NotEmailError('Wrong e-mail address has been provided')

    return True


def check_age(age: int) -> bool:
    """
        Функция проверяет передданную переменную на соответствие условию 10 <= age <= 99
        В случае не соответствия вызывает исключение ValueError
    :param age: Целочисленная переменная
    :return: True в случае успеха
    """
    if age < 10 or age > 99:
        raise ValueError('Provided age is not permitted')

    return True


def check_line(str_line: str) -> bool:
    """
        Фунция принимает для анализа строку в формате "<Name> <E-Mail> <Age>"
        И разбивает ее на соответсвующие части для дальнейшего анализа.
        В случае если строка не имеет указанный формат вызывает исключение ValueError.
    :param str_line: Строковая переменная в выщеуказанном формате.
    :return: True в случае успеха, в противном случае возвращает False.
    """
    try:
        name, email, age = str_line.split(' ')
    except ValueError:
        raise ValueError('Some information is missed')
    else:
        if check_name(name=name) and check_email(email=email) and check_age(age=int(age)):
            return True

    return False


input_file, good_records, bad_records = None, None, None

try:
    input_file = open('registrations.txt', 'r', encoding='utf8')
    good_records = open('registrations_good.log', 'w', encoding="utf8")
    bad_records = open('registrations_bad.log', 'w', encoding="utf8")
except OSError:
    print('Cannot open the file!')
else:
    if input_file is not None:
        line = input_file.readline()
        while line:
            try:
                check_line(line)
            except (ValueError, NotNameError, NotEmailError) as exc:
                bad_records.write(f'{line[:-1]} - {exc}\n')
            else:
                good_records.write(line)
            line = input_file.readline()
finally:
    if input_file is not None:
        input_file.close()

    if good_records is not None:
        good_records.close()

    if bad_records is not None:
        bad_records.close()
