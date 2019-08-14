# -*- coding: utf-8 -*-

# Написать декоратор, который будет логировать (записывать в лог файл)
# ошибки из декорируемой функции и выбрасывать их дальше.
#
# Имя файла лога - function_errors.log
# Формат лога: <имя функции> <параметры вызова> <тип ошибки> <текст ошибки>
# Лог файл открывать каждый раз при ошибке в режиме 'a'
from termcolor import cprint


def log_errors(filename: str):
    """
        Функция создает декоратор. Создаваемый декоратор перехватывает иключения,
        возникающие в декорируемой функции и записывает их в файл,
        имя которого получает в качестве параметра данная функция.
    :param filename: Имя создаваемого файла
    :return: Функцию-декоратор
    """

    def log_decorator(func):
        def surrogate(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except (ValueError, ZeroDivisionError) as exc:
                try:
                    file = open(filename, 'a', encoding='utf8')
                except IOError:
                    cprint(f'Cannot open the file "{filename}"')
                    raise SystemExit
                else:
                    file.write(f'The function "{func.__name__}" with parameters: {args}, {kwargs} '
                               f'has raised the following exception: {exc}\n')
                    file.close()
            else:
                return result
        return surrogate

    return log_decorator

# Проверить работу на следующих функциях
@log_errors(filename='function_errors.log')
def perky(param):
    return param / 0


@log_errors(filename='function_errors.log')
def check_line(str_line):
    name, email, age = str_line.split(' ')
    if not name.isalpha():
        raise ValueError("it's not a name")
    if '@' not in email or '.' not in email:
        raise ValueError("it's not an email")
    if not 10 <= int(age) <= 99:
        raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]
for line in lines:
    try:
        check_line(line)
    except Exception as exc:
        print(f'Invalid format: {exc}')
perky(param=42)


# Усложненное задание (делать по желанию).
# Написать декоратор с параметром - именем файла
#
# @log_errors('function_errors.log')
# def func():
#     pass

