"""
    Модуль для работы с прогнозом погоды
"""
# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database
import datetime
from weather import WeatherMaker, DatabaseUpdater, DayWeather
from argparse import ArgumentParser


class CMDParser(ArgumentParser):
    """
        Класс работает с командной строкой.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_argument('command', choices=['read', 'add'],
                          type=str, help="Command. What the script should do with data")
        self.add_argument('start', type=self.convert_date, help="Start from this date. Example: 20/12/2020")
        self.add_argument('finish', type=self.convert_date, help="Finish with this date. Example: 30/12/2020")
        self.add_argument('--display', choices=['postcard', 'console'],
                          type=str, help="The device to display. Available values: postcards/console (p/c)")

        self.description = 'The script is displaying (if using "read" command) the weather condition ' \
                           'for indicating dates. When using "add" command information about the weather conditions ' \
                           'will be parsed from Internet and added into the database.'

    @staticmethod
    def convert_date(date: str) -> datetime.date:
        """
            Метод возварщает полученный аргумент в виде даты
        :param date:
        :return:
        """
        day, month, year = map(int, date.split("/"))

        return datetime.date(year, month, day)


class InformationDesk:
    """
        Работает с WeatherMaker и DatabaseUpdater.
        Получает информацию о погоде из базы данных или парсит из Интернета.
        Выводит на консоль или сохраняет в виде графических информеров-открыток на диске.
    """
    mode: str
    start: datetime.date
    finish: datetime.date
    output: str
    updater: DatabaseUpdater
    weather: WeatherMaker

    def __init__(self, mode: str, start: datetime.date, finish: datetime.date, output: str = 'console'):
        self.mode = mode
        self.start = start
        self.finish = finish
        self.output = output
        self.updater = DatabaseUpdater(url='sqlite:///weather.db')
        self.weather = WeatherMaker()

        for day in self.weather:
            self.updater.update(day_record=day)

        self.weather.setup_date_range(from_date=self.start, to_date=self.finish)

    def output_data(self, data: DatabaseUpdater):
        """
            Выводит полученные данные
        :return: none
        """
        if self.output == 'console':
            for day in data:
                print(f'Дата: {day.Date}')
                print(f'{"Температура:":^15}{"Давление:":^15}{"Влажность:":^15}{"Ветер:":^25}{"Условия:":^45}')
                print(f'{"Днем:":>10}'
                      f'{day.Temp_day:>5}'
                      f'{day.Pressure:^15}'
                      f'{day.Humidity:^15}'
                      f'{"Скорость:":>15}'
                      f'{day.Wind_speed:>10}'
                      f'{day.Conditions:^45}')
                print(f'{"Ночью:":>10}'
                      f'{day.Temp_night:>5}'
                      f'{"":^15}'
                      f'{"":^15}'
                      f'{"Направление:":>15}'
                      f'{day.Wind_direction:>10}')
                print(f'{"Ощущается:":>10}'
                      f'{day.Temp_feels_like:>5}'
                      f'{"":^15}'
                      f'{"":^15}'
                      f'{"Порывы:":>15}'
                      f'{day.Wind_gust:>10}')
        else:
            record = DayWeather()

            for day in data:
                record.day_weather_info['date'] = day.Date
                record.day_weather_info['image'] = day.Image
                record.day_weather_info['temp'] = DayWeather.Temperature(
                    _temp_day='+' + str(day.Temp_day) if day.Temp_day > 0 else '-' + str(day.Temp_day),
                    _temp_night='+' + str(day.Temp_night) if day.Temp_night > 0 else '-' + str(day.Temp_night),
                    _temp_feels_like='+' +
                                     str(day.Temp_feels_like) if day.Temp_feels_like > 0 else '-'
                                                                                              + str(day.Temp_feels_like)
                )
                record.day_weather_info['pressure'] = str(day.Pressure)
                record.day_weather_info['humidity'] = day.Humidity
                record.day_weather_info['wind'] = DayWeather.Wind(
                    wind_speed=day.Wind_speed,
                    wind_direction=day.Wind_direction,
                    wind_gust=day.Wind_gust
                )
                record.day_weather_info['conditions'] = day.Conditions.split(", ")

                record.informer.save_to_disk()

    def save_to_database(self) -> None:
        """
            Сохраняет данные в базу данных
        :return:
        """
        for day in self.weather.days:
            self.updater.update(day_record=day)

    def get_data(self):
        """
            Получает данные для вывода
        :return:
        """
        if self.mode != 'read':
            self.save_to_database()

        return self.updater.select(self.start, self.finish)

    def run(self):
        """
            Запускает процесс
        :return:
        """
        data_for_output = self.get_data()
        self.output_data(data=data_for_output)


def main():
    """
        Функция main
    """

    parser = CMDParser()
    args = parser.parse_args()

    desk = InformationDesk(mode=args.command, start=args.start, finish=args.finish, output=args.display)
    desk.run()


if __name__ == '__main__':
    main()
