# TODO: Create a class for storing the database in RAM
from civil import *
from military import *
import operator
import re
import os, sys


def convert_regex_to_line(line):
    new_line = ""
    for i in line:
        new_line += f"[{i}]\t"
    return new_line


class Database:
    directory = ""

    def __init__(self, directory: str):
        self.error = False
        self.error_index = None
        self._persons = []
        index = 0
        Database.directory = directory
        with open(directory, "r+") as database:
            self._database = database.readlines()
        if self._database:
            for line in self._database:
                if line[0] == "\n":
                    self._database[index] = ""
                    continue
                if line[0] == "#":
                    continue
                line = re.findall("\[(.*?)]", line)
                birthdate = line[4].split("-")
                birthdate = date(int(birthdate[0]), int(birthdate[1]), int(birthdate[2]))
                self._persons.append(Civil(name=line[1], surname=line[2], patronymic=line[3],
                                           birthdate=birthdate, height=line[5], weight=line[6], location=line[7],
                                           number=line[8], education=line[9], reserver=line[10], civil_occupation=line[11],
                                           military_speciality=line[12], rank=line[13], rank_assignment_date=line[14],
                                           position=line[15], subdivision=line[16], duty_form=line[17],
                                           character_note=line[18], attitude_to_duty=line[19], is_appropriate=line[20]) if
                                     line[0] == "Civil" else
                                     Military(name=line[1], surname=line[2], patronymic=line[3],
                                              birthdate=birthdate, height=line[5], weight=line[6], location=line[7],
                                              number=line[8], education=line[9], military_speciality=line[10],
                                              rank=line[11], rank_assignment_date=line[12],
                                              position=line[13], subdivision=line[14], duty_form=line[15],
                                              character_note=line[16], attitude_to_duty=line[17]))

                index += 1
            if Civil.error == True or Military.error == True:
                self.error = True
            self.sort()
        else:
            pass

    def delete_line(self, line: str):
        try:
            self._database.remove(line)
        except ValueError:
            return -1

    @property
    def database(self):
        return self._database

    @property
    def persons(self):
        return self._persons

    def save(self):
        to_be_saved = ""
        index = 0
        try:
            for person in self._persons:
                to_be_saved += person.str() + "\n"
                index += 1
        except Exception:
            self.error = True
            self.error_index = index
            with open(Database.directory, "w+") as database:
                database.writelines(self._database)
        if not self.error:
            with open(Database.directory, "w+") as database:
                database.writelines(to_be_saved)

    def save_after_error(self, wrong_line: str):
        if self.error:
            with open(self.directory, "w") as database:
                for i in self._database:
                    database.write(i + "\n")

    def sort(self, parameter="surname", reverse=False):
        try:
            self._persons.sort(reverse=reverse, key=operator.attrgetter(parameter))
        except Exception:
            self.error = True
            show_error("Щось пішло не так із сортуванням...")
        self.save()


if __name__ == '__main__':
    db = Database("./database.txt")
