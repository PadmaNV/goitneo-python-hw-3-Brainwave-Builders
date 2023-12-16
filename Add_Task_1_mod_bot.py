import pickle
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)
            return "Phone added."
        except ValueError as e:
            return str(e) and print("Invalid phone number format")

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)
                return "Phone removed."
        return "Phone not found."

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                try:
                    phone_obj.value = new_phone
                    return "Phone edited."
                except ValueError as e:
                    return str(e)
        return "Phone not found."

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
            return "Birthday added."
        except ValueError as e:
            return str(e)

    def show_birthday(self):
        return str(self.birthday) if self.birthday else "Birthday not set."

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {self.show_birthday()}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return "Contact deleted."
        else:
            return "Contact not found."

    def get_birthdays_per_week(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        birthdays = []

        for record in self.data.values():
            if record.birthday:
                b_date = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                birthday_this_year = b_date.replace(year=today.year)
                if today <= birthday_this_year < next_week:
                    birthdays.append(record)

        return birthdays

    def save_to_disk(self, filename="address_book.pkl"):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_disk(self, filename="address_book.pkl"):
        try:
            with open(filename, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            # If the file is not found, create an empty dictionary
            self.data = {}

# Функції-обробники команд:
def add_birthday_command(book, name, birthday):
    record = book.find(name)
    if record:
        return record.add_birthday(birthday)
    else:
        return "Contact not found."

def show_birthday_command(book, name):
    record = book.find(name)
    if record:
        return record.show_birthday()
    else:
        return "Contact not found."

def birthdays_command(book):
    birthdays = book.get_birthdays_per_week()
    if birthdays:
        return "\n".join(str(record) for record in birthdays)
    else:
        return "No birthdays in the next week."

# Код бота:
book = AddressBook()

# Завантаження даних з файлу 
book.load_from_disk()

while True:
    command = input("Enter command: ").split()

    if command[0] == "add":
        name, phone = command[1], command[2]
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        print("Contact added.")

    elif command[0] == "change":
        name, new_phone = command[1], command[2]
        record = book.find(name)
        if record:
            print(record.edit_phone(record.phones[0].value, new_phone))
        else:
            print("Contact not found.")

    elif command[0] == "phone":
        name = command[1]
        record = book.find(name)
        if record:
            print(record.phones[0])
        else:
            print("Contact not found.")

    elif command[0] == "all":
        for record in book.data.values():
            print(record)

    elif command[0] == "add-birthday":
        name, birthday = command[1], command[2]
        print(add_birthday_command(book, name, birthday))

    elif command[0] == "show-birthday":
        name = command[1]
        print(show_birthday_command(book, name))

    elif command[0] == "birthdays":
        print(birthdays_command(book))

    elif command[0] == "save":
        book.save_to_disk()
        print("Address book saved to disk.")

    elif command[0] == "load":
        book.load_from_disk()
        print("Address book loaded from disk.")

    elif command[0] == "hello":
        print("Hello!")

    elif command[0] == "close" or command[0] == "exit":
        break

    else:
        print("Invalid command.")
