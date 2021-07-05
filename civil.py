from personal_data import *


class Civil(PersonalData):

    attr_list = ["name", "surname", "patronymic", "birthdate", "height", "weight", "location", "number",
                 "education", "reserver", "civil_occupation", "military_speciality", "rank", "rank_assignment_date", "position",
                 "subdivision", "duty_form", "character_note", "attitude_to_duty", "is_appropriate"]

    def __init__(self, name=None, surname=None, patronymic=None, birthdate=None, height=None, weight=None,
                 location=None, number=None, education=None, reserver=None, civil_occupation=None,
                 military_speciality=None, rank=None,
                 rank_assignment_date=None, position=None, subdivision=None, duty_form=None, character_note=None,
                 attitude_to_duty=None, is_appropriate=None, **kwargs):
        super(Civil, self).__init__(name, surname, patronymic, birthdate, height, weight, location, number, education)
        self.reserver = reserver
        self.civil_occupation = civil_occupation
        self.military_speciality = military_speciality
        self.rank = rank
        self.rank_assignment_date = rank_assignment_date
        self.position = position
        self.subdivision = subdivision
        self.duty_form = duty_form
        self.character_note = character_note
        self.attitude_to_duty = attitude_to_duty
        self.is_appropriate = is_appropriate

    # __________________________RESERVER______________________ #
    @property
    def reserver(self):
        return self._reserver

    @reserver.setter
    def reserver(self, value):
        try:
            if isinstance(value, str):
                self._reserver = value
            elif value is None:
                self._reserver = "Дані відсутні"
            else:
                raise ValueError("Некорректно введені дані щодо буття офіцером запасу")
        except ValueError as err:
            show_error(err)
            Civil.error = True

        # ____________________________________________________ #

    # __________________________CIVIL_OCCUPATION______________________ #
    @property
    def civil_occupation(self):
        return self._civil_occupation

    @civil_occupation.setter
    def civil_occupation(self, value):
        try:
            if isinstance(value, str):
                self._civil_occupation = value
            elif value is None:
                self._civil_occupation = "Дані відсутні"
            else:
                raise ValueError("Некорректно введені дані цивільної зайнятості")
        except ValueError as err:
            show_error(err)
            Civil.error = True

    # ____________________________________________________ #

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
            Civil.error = True

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
            Civil.error = True

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
            Civil.error = True

    # ____________________________________________________ #

    # __________________________POSITION______________________ #
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: str):
        try:
            self._position = value
        except ValueError as err:
            show_error(err)
            Civil.error = True

    # ____________________________________________________ #

    # __________________________SUBDIVISION______________________ #
    @property
    def subdivision(self):
        return self._subdivision

    @subdivision.setter
    def subdivision(self, value: str):
        try:
            self._subdivision = value
        except ValueError as err:
            show_error(err)
            Civil.error = True

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
            Civil.error = True

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
            Civil.error = True

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
            Civil.error = True

    # ____________________________________________________ #

    # __________________________IS_APPROPRIATE______________________ #
    @property
    def is_appropriate(self):
        return self._is_appropriate

    @is_appropriate.setter
    def is_appropriate(self, value: bool):
        try:
            self._is_appropriate = value
        except ValueError as err:
            show_error(err)
            Civil.error = True

    # ____________________________________________________ #

    def str(self):
        return f"[{self.__class__.__name__}]    [{self._name}] [{self._surname}]   [{self._patronymic}]   [{self.birthdate}]  " \
               f"[{self._height}]   [{self._weight}] [{self._location}] [{self._number}]   [{self._education}]   " \
               f"[{self._reserver}]  [{self._civil_occupation}]  " \
               f"[{self._military_speciality}]  [{self._rank}]  [{self._rank_assignment_date}]  " \
               f"[{self._position}] [{self._subdivision}]   [{self._duty_form}] [{self._character_note}]    " \
               f"[{self._attitude_to_duty}] [{self._is_appropriate}]"

    def __str__(self, city=None):
        if city is None:
            return f"{self.surname}    {self.name}  {self.patronymic}   {self.birthdate}    Цивільний"
        else:
            return f"{self.surname}    {self.name}  {self.patronymic}   {self.birthdate}    Цивільний   {self._location.city}"

    @staticmethod
    def ToMilitary(person):
        if isinstance(person, Civil):
            return Military(person.name, person.surname, person.patronymic, person._birthdate, person.height,
                         person.weight, person.location, person.number, person.education,
                         person.military_speciality, person.rank, person.rank_assignment_date, person.position,
                         person.subdivision, person.duty_form, person.character_note, person.attitude_to_duty)
        else:
            show_error("Помилка при перетворенні цивільного на військового.")


if __name__ == '__main__':
    civil = Civil("денис", "матій", "батькович", "2003-02-06", "195", "56",
                  "90361, Закарпат, виноградівс, Чепа, дружбт, 2", "+380956809995", "ЧНУ", False)
    print(civil)
    print(civil.__str__(1))
