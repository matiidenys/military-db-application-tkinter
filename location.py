allowedLetters = "йцукенгшщзфівапролдхїґжєячсмитьбю-' "


class Location:
    def __init__(self, index: str, state: str, district: str, city: str, street: str, number: str):
        elements = [state, district, city, street]
        for el in elements:
            el = el.lower()
            for letter in el:
                if not allowedLetters.__contains__(letter):
                    raise ValueError("Неправильно введена адреса.")
        self.index = int(index)
        self.state = state
        self.district = district
        self.city = city
        self.street = street
        self.number = number

    def __str__(self):
        return f"{self.index}, {self.state}, {self.district}, {self.city}, {self.street}, {self.number}"
