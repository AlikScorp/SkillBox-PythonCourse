from random import sample

number = ''


def generate_number(quantity):
    global number

    while True:
        number = sample(''.join(map(str, range(10))), quantity)
        if number[0] != '0':
            break


def check_number(num):
    result = {'bulls': 0, 'cows': 0}
    for i, figure in enumerate(num):
        if figure in number:
            if i == number.index(figure):
                result['bulls'] += 1
            else:
                result['cows'] += 1
    return result


if __name__ == "__main__":
    generate_number(4)
    print(number)
    print(check_number('2345'))
