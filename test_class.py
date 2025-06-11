class Person:
    def __init__(self, name):
        self.name = f"dfghj {name}"  # имя человека


tom = Person("Tom")

# обращение к атрибутам
# получение значений
print(tom.name)  # Tom

from datetime import datetime

# Получаем текущую дату
now = datetime.now()
# Форматируем дату: полное название месяца и год
current_month_year = now.strftime("%m %Y")

print(current_month_year)

a = None
if not a:print(1)