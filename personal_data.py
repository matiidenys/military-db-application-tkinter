from datetime import date, datetime
from location import Location
from show_error import show_error
from abc import ABC
from database import *

allowedLetters = "йцукенгшщзфівапролдхїґжєячсмитьбю-' "


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class PersonalData(ABC):
    error = False

    def __init__(self, name=None, surname=None, patronymic=None, birthdate=None, height=None, weight=None,
                 location=None, number=None, education=None):
        self.name = name  # Ім'я
        self.surname = surname  # Прізвище
        self.patronymic = patronymic  # По батькові
        self.birthdate = birthdate  # Рік народження
        self.height = height  # Висота
        self.weight = weight  # Вага
        self.location = location  # Прописка
        self.number = number  # Номер телефону
        self.education = education
        self._age = calculate_age(self._birthdate)

    # __________________________NAME______________________ #
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        try:
            value = value.lower()
            for letter in value:
                if not allowedLetters.__contains__(letter):
                    raise ValueError("Введено заборонений символ.")
            self._name = value.upper()
        except ValueError as err:
            show_error(err)
            PersonalData.error = True

    # ____________________________________________________ #

    # __________________________SURNAME______________________ #
    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        try:
            value = value.lower()
            for letter in value:
                if not allowedLetters.__contains__(letter):
                    raise ValueError("Введено заборонений символ.")
            self._surname = value.upper()
        except ValueError as err:
            show_error(err)
            PersonalData.error = True

    # ____________________________________________________ #

    # __________________________PATRONYMIC______________________ #
    @property
    def patronymic(self):
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value):
        try:
            value = value.lower()
            for letter in value:
                if not allowedLetters.__contains__(letter):
                    raise ValueError("Введено заборонений символ.")
            self._patronymic = value.upper()
        except ValueError as err:
            show_error(err)
            PersonalData.error = True

    # ____________________________________________________ #

    # __________________________BIRTHDATE______________________ #
    @property
    def birthdate(self):
        return self._birthdate.strftime("%Y-%m-%d")

    @birthdate.setter
    def birthdate(self, value):
        try:
            if isinstance(value, date):
                if datetime.now().year < value.year:
                    raise ValueError("Введено майбутній час.")
                self._birthdate = value
            if isinstance(value, str):
                try:
                    value = value.split("-")
                    value = date(int(value[0]), int(value[1]), int(value[2]))
                except Exception:
                    raise ValueError("Неправильно введені дані дня народження.")
                if value.year < 1900:
                    raise ValueError("Вказано рік, нижчий за 1900.")
                if datetime.now().year < value.year:
                    raise ValueError("Введено майбутній час.")
                self._birthdate = value
                today = datetime.now()
                self._age = today.year - self._birthdate.year - ((today.month, today.day) < (self._birthdate.month,
                                                                                             self._birthdate.day))

        except ValueError as err:
            show_error(err)
            PersonalData.error = True

    # ____________________________________________________ #

    # __________________________AGE______________________ #
    @property
    def age(self):
        return self._age


    # ____________________________________________________ #

    # __________________________HEIGHT______________________ #
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        try:
            value = int(value)
            if value < 30 or value > 300:
                raise ValueError
            self._height = value
        except Exception:
            show_error("Некорректні дані щодо зросту.")
            PersonalData.error = True

    # ____________________________________________________ #

    # __________________________WEIGHT______________________ #
    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        try:
            value = int(value)
            if value < 10 or value > 250:
                raise ValueError
            self._weight = value
        except Exception:
            show_error("Некорректні дані щодо ваги.")
            PersonalData.error = True

    # ____________________________________________________ #

    # __________________________LOCATION______________________ #
    @property
    def location(self):
        return self._location.__str__()

    @location.setter
    def location(self, value):
        try:
            if isinstance(value, str):
                location = value.split(", ")
                value = Location(location[0], location[1], location[2], location[3], location[4], location[5])
            self._location = value
        except ValueError as err:
            show_error(err)
            PersonalData.error = True

    # ____________________________________________________ #

    # __________________________NUMBER______________________ #
    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        try:
            if value[:4] != "+380" or len(value) != 13:
                raise ValueError("Некорректно введений номер телефону.")
            self._number = value
        except ValueError as err:
            show_error(err)
            PersonalData.error = True

    # ____________________________________________________ #

    # __________________________EDUCATION______________________ #
    @property
    def education(self):
        return self._education

    @education.setter
    def education(self, value):
        try:
            if isinstance(value, str):
                self._education = value
            elif value is None:
                self._education = "Дані відсутні"
            else:
                raise ValueError("Некорректно введені дані освіти")
        except ValueError as err:
            show_error(err)
            PersonalData.error = True

    # ____________________________________________________ #

    def type(self):
        return self.__class__.__name__
