import datetime as dt
# Импорт модуля, который потом не используется. Нужно удалить
import json

# Отступ между блоком импорта и остальным кодом должен быть 2 строки.
# Нужно добавить пустую строку
class Record:
    def __init__(self, amount, comment, date=''):
        # Оператор '=' при присваивании следует окружать пробелами.
        # Правильный вариант: self.amount = amount
        # Ниже эта ошибка встречаеся несколько раз, прошу обратить внимание
        self.amount=amount
        # Обычно принято под if ставить неотрицательное условие
        # и т.к. строка 20 вышла слишком грамоздкой (больше 80 символов),
        # лучше сделать if в многострочном виде как ниже.
        # if date:
        #     self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        # else:
        #     dt.datetime.now().date()
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment=comment
class Calculator:
    def __init__(self, limit):
        self.limit = limit
        # Т. к. мы заранее знаем тип объектов, которые будут храниться в
        # списке, желательно применить аннотацию self.records:List[Record] = []
        # но перед этим естетственно нужно заимпортировать List:
        # from typing import List
        self.records=[]
    def add_record(self, record):
        self.records.append(record)
    def get_today_stats(self):
        today_stats=0
        for Record in self.records:
            # Сегодняшнюю дату лучше вынести в отдельную переменную,
            # как это сделано в методе get_week_stats
            if Record.date == dt.datetime.now().date():
                # Оператор + следует окружить пробелами
                today_stats = today_stats+Record.amount
        return today_stats
    def get_week_stats(self):
        week_stats=0
        today = dt.datetime.now().date()
        for record in self.records:
            # Ошибки с пробелами.
            # Ими нужно окружать все операторы в выражениях.
            # Причем слева и справа должно стоять тоько по одному пробелу.
            # Здесь такие проблемы с операторами: '-', '<', '>=', '+='
            # Вторая проверка на >= 0 - лишняя
            if (today -  record.date).days <7 and (today -  record.date).days >=0:
                week_stats +=record.amount
        return week_stats
class CaloriesCalculator(Calculator):
    def get_calories_remained(self): # Получает остаток калорий на сегодня
        x=self.limit-self.get_today_stats()
        if x > 0:
            # Строка ниже переходит за 80 символов, поэтому ее нужно разбить.
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        else:
            return 'Хватит есть!'
class CashCalculator(Calculator):
    # После # следует оставлять пробел
    USD_RATE=float(60) #Курс доллар США.
    EURO_RATE=float(70) #Курс Евро.
    # Здесь не нужно передавать константы в метод, так как они заданы в классе,
    # значит к ним можно обращаться через self. Например self.USD_RATE.
    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Ненужное присваивание, ниже при сравнении можно использовать currency
        currency_type=currency
        cash_remained = self.limit - self.get_today_stats()
        # Необходимы пробелы перед оператором сравнения
        if currency=='usd':
            cash_remained /= USD_RATE
            # Было бы лаконичнее завести словарь с типами валют и их названием
            # currency_type = {'usd': 'USD', 'eur': 'Euro', ...}
            # Тогда можно взять currency_type перед блоком if, так:
            # currency_name = currency_type[currency]
            currency_type ='USD'
        elif currency_type=='eur':
            cash_remained /= EURO_RATE
            currency_type ='Euro'
        elif currency_type=='rub':
            # Ошибка. В случае с рублем не нужно делать ничего
            cash_remained == 1.00
            currency_type ='руб'
        if cash_remained > 0:
            # Строка переходит за 80 символов. Как вариант, можно
            # вынести операцию округлеения на отдельню строку. Вот так:
            # rounded_cash = round(cash_remained, 2)
            # return f'На сегодня осталось {rounded_cash} {currency_type}'
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Лучше использовать тип форматирования как в elif выше,
            # он понятнее и короче.
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)

    # Нет необходимости перегружать метод, если внитри него затем вызывается
    # этот же метод родительского класса. Если удалить этот код,
    # ничего не поменяется
    def get_week_stats(self):
        super().get_week_stats()

# Общие замечания:
#
# - Если атрибут класса используется только внутри класса следует сделать его
# непубличным, т.е. добавить символ подчеркивания перед названием. Пример
# self._amount = amount
#
# - Перед комментариями, оставленными на той же строке, что и код,
# следует оставлять два пробела перед #. Например в 54 строчке следует сделать
# так:
# def get_calories_remained(self):  # Получает остаток калорий на сегодня
#
# - Классы следует разделять двумя пустыми строками
#
# - Между методами внутри класса следует оставлять пустую строку
