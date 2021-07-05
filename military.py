from personal_data import *
from civil import *


class Military(PersonalData):

    attr_list = ["name", "surname", "patronymic", "birthdate", "height", "weight", "location", "number",
                 "education", "military_speciality", "rank", "rank_assignment_date",
                 "position", "subdivision", "duty_form", "character_note", "attitude_to_duty"]

    def __init__(self, name=None, surname=None, patronymic=None, birthdate=None, height=None, weight=None,
                 location=None, number=None, education=None, military_speciality=None, rank=None,
                 rank_assignment_date=None, position=None, subdivision=None, duty_form=None, character_note=None,
                 attitude_to_duty=None, **kwargs):
        super(Military, self).__init__(name, surname, patronymic, birthdate, height, weight, location, number,
                                       education)
        self.military_speciality = military_speciality
        self.rank = rank
        self.rank_assignment_date = rank_assignment_date
        self.position = position
        self.subdivision = subdivision
        self.duty_form = duty_form
        self.character_note = character_note
        self.attitude_to_duty = attitude_to_duty

    # __________________________MILITARY_SPECIALITY______________________ #
    @property
    def military_speciality(self):
        return self._military_speciality

    @military_speciality.setter
    def military_speciality(self, value):
        try:
            if isinstance(value, str):
                self._military_speciality = value
            elif value is None:
                self._military_speciality = "Дані відсутні"
            else:
                raise ValueError("Некорректно введені дані військової спеціальності")
        except ValueError as err:
            show_error(err)
            Military.error = True

    # ____________________________________________________ #

    # __________________________RANK______________________ #
    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        try:
            if isinstance(value, str):
                self._rank = value
            elif value is None:
                self._rank = "Дані відсутні"
            else:
                raise ValueError("Некорректно введені дані звання")
        except ValueError as err:
            show_error(err)
            Military.error = True

    # ____________________________________________________ #

    # __________________________RANK_ASSIGNMENT_DATE______________________ #
    @property
    def rank_assignment_date(self):
        return self._rank_assignment_date

    @rank_assignment_date.setter
    def rank_assignment_date(self, value):
        try:
            if isinstance(value, date):
                self._rank_assignment_date = value.strftime("%d.%m.%Y")
            elif isinstance(value, str):
                self._rank_assignment_date = value
            elif value is None:
                self._rank_assignment_date = "Дані відсутні"
            else:
                raise ValueError("Некорректно введені дані дати присвоєння звання")
        except ValueError as err:
            show_error(err)
            Military.error = True

    # ____________________________________________________ #

    # __________________________POSITION______________________ #
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: str):
        try:
            if isinstance(value, str):
                self._position = value
            elif value is None:
                self._position = "Нема даних"
            else:
                raise ValueError("Неправильно введена посада")
        except ValueError as err:
            show_error(err)
            Military.error = True

    # ____________________________________________________ #

    # __________________________SUBDIVISION______________________ #
    @property
    def subdivision(self):
        return self._subdivision

    @subdivision.setter
    def subdivision(self, value: str):
        try:
            if isinstance(value, str) and value != "":
                self._subdivision = value
            elif value is None or value == "":
                self._subdivision = "Нема даних"
            else:
                raise ValueError("Неправильно введений підрозділ")
        except ValueError as err:
            show_error(err)
            Military.error = True

    # ____________________________________________________ #

    # __________________________DUTY_FORM______________________ #
    @property
    def duty_form(self):
        return self._duty_form

    @duty_form.setter
    def duty_form(self, value: str):
        try:
            self._duty_form = value
        except ValueError as err:
            show_error(err)
            Military.error = True

    # ____________________________________________________ #

    # __________________________CHARACTER_NOTE______________________ #
    @property
    def character_note(self):
        return self._character_note

    @character_note.setter
    def character_note(self, value: str):
        try:
            self._character_note = value
        except ValueError as err:
            show_error(err)
            Military.error = True

    # ____________________________________________________ #

    # __________________________ATTITUDE_TO_DUTY______________________ #
    @property
    def attitude_to_duty(self):
        return self._attitude_to_duty

    @attitude_to_duty.setter
    def attitude_to_duty(self, value: str):
        try:
            self._attitude_to_duty = value
        except ValueError as err:
            show_error(err)
            Military.error = True

    # ____________________________________________________ #

    def str(self):
        return f"[{self.__class__.__name__}]    [{self._name}] [{self._surname}]   [{self._patronymic}]   [{self.birthdate}]  " \
               f"[{self._height}]   [{self.weight}] [{self._location}] [{self._number}]    [{self._education}] " \
               f"[{self._military_speciality}]  [{self._rank}] [{self._rank_assignment_date}] " \
               f"[{self._position}] [{self._subdivision}]   [{self._duty_form}] [{self._character_note}]    " \
               f"[{self._attitude_to_duty}]"

    def __str__(self, city=None):
        if city is None:
            return f"{self.surname}    {self.name}  {self.patronymic}   {self.birthdate}    Військовий"
        else:
            return f"{self.surname}    {self.name}  {self.patronymic}   {self.birthdate}    Військовий  {self._location.city}"

    @staticmethod
    def ToCivil(person):
        if isinstance(person, Military):
            return Civil(person.name, person.surname, person.patronymic, person._birthdate, person.height,
                         person.weight, person.location, person.number, person.education, "True", None,
                         person.military_speciality, person.rank, person.rank_assignment_date, person.position,
                         person.subdivision, person.duty_form, person.character_note, person.attitude_to_duty)
        else:
            show_error("Помилка при перетворенні війського на цивільного.")
