from collections import UserDict
from validation import *


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __repr__(self) -> str:
        return f"{self.value}"

    def __str__(self) -> str:
        return f"{self.value}"

    def __eq__(self, __o: object) -> bool:
        if self.value == __o.value:
            return True
        return False


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = phone_number_validation(value)


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = birthday_validation(value)


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def __repr__(self):
        return f"{self.name.value} {','.join([p.value for p in self.phones]) if self.phones else ''}" \
               f" {self.birthday if self.birthday else ''}"

    def add(self, phone: Phone):
        if isinstance(phone, Phone):
            self.phones.append(phone)
        return f"phone {phone.value} add successful to contact {self.name.value}"

    def edit(self, old_phone, new_phone):
        if old_phone in self.phones:
            self.phones.remove(old_phone)
            self.phones.append(new_phone)
        else:
            print(f"In this record no phone {old_phone}")

    def remove(self, old_phone):
        if old_phone in self.phones:
            self.phones.remove(old_phone)
        else:
            print(f"In this record no phone {old_phone}")

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today().date()
            next_birthday = self.birthday.value.replace(year=today.year)
            if today < next_birthday:
                gap = (next_birthday - today).days
                return "This contact birthday is in " + str(gap) + " days."
            elif today == next_birthday:
                return "Today is contact's birthday! Happy Birthday!"
            else:
                next_birthday = self.birthday.value.replace(year=today.year + 1)
                gap = (next_birthday - today).days
                return "This contact birthday is in " + str(gap) + " days."
        else:
            return "Current contact doesn't have date of birth"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.index = None

    def add_record(self, record: Record):
        self.index = len(self.data) + 1
        self.data[record.name.value] = record

    def show(self, start=1, end=1):
        if start <= end <= len(self.data):
            key = list(self.data.keys())
            while start <= end:
                record = self.data[key[start]]
                yield f"{record.name}: {', '.join([p.value for p in record.phones]) if record.phones else ''}" \
                      f" {record.birthday if record.birthday else ''}"
                start += 1
        else:
            print(f"Value 'end' {end} is more than numbers of Address Book")

    def __repr__(self):
        return f"{self.data}"

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        keys = tuple(self.data.keys())
        if self.index == len(self):
            raise StopIteration
        key = keys[self.index]
        record = self.data[key]
        self.index += 1
        return f"{record.name}: {', '.join([p.value for p in record.phones]) if record.phones else ''} " \
               f"{record.birthday if record.birthday else ''}"


if __name__ == "__main__":
    ab = AddressBook()
    name1 = Name("Bill")
    phone1 = Phone("+380996787877")
    rec1 = Record(name1, phone1)

    rec2 = Record(Name("Jill"), Phone("+389671234545"), Birthday("12.03.1995"))

    ab.add_record(rec1)
    ab.add_record(rec2)

    phone3 = Phone("045342343422")

    rec1.add(phone3)

    phone4 = Phone("+380996787878")
    phone5 = Phone("+380667877676")

    rec1.edit(phone1, phone5)

    print(ab["Jill"].days_to_birthday())

    print(ab)

    ab["Bill"].remove(phone3)

    for k in ab:
        print(k)

    show = ab.show(0, 0)
    for i in show:
        print(i)
