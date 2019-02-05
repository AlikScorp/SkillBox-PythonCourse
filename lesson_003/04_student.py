# -*- coding: utf-8 -*-

# (цикл while)

# Ежемесячная стипендия студента составляет educational_grant руб., а расходы на проживание превышают стипендию
# и составляют expenses руб. в месяц. Рост цен ежемесячно увеличивает расходы на 3%, кроме первого месяца
# Составьте программу расчета суммы денег, которую необходимо единовременно попросить у родителей,
# чтобы можно было прожить учебный год (10 месяцев), используя только эти деньги и стипендию.
# Формат вывода:
#   Студенту надо попросить ХХХ.ХХ рублей

educational_grant, expenses = 10000, 12000
i = 1
total_expenses = 0
parents_grant = 0
school_year = 10

while i <= school_year:
    total_expenses += expenses
    expenses += expenses*.03
    i += 1

parents_grant = total_expenses - school_year * educational_grant
print('Студенту надо попросить', round(parents_grant, 2), 'рублей')

# другой вариант

educational_grant, expenses = 10000, 12000
i = 1
total_expenses = 0
parents_grant = 0
school_year = 10

while i <= school_year:
    parents_grant += expenses - educational_grant
    expenses += expenses*.03
    i += 1

print('Студенту надо попросить', round(parents_grant, 2), 'рублей')

# зачет!
