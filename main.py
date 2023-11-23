from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        self.__value = value
        
    def __eq__(self, other):
       return self.__value == other.__value
            
    def __repr__(self):
        return str(self.__value)    

 
class Name(Field):    
    def __init__(self, value):
        self.__value = None
        self.value = value
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):        
        if new_value.isalpha():    
            self.__value = new_value
        else:
            raise Exception('Wrong name!')

class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if len(new_value) == 10:
            if new_value.isdigit():
                self.__value = new_value
            else:
                raise ValueError('Invalid literal in phone number!')
        else:
            raise Exception('Wrong phone number!')
        
class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value
        super().__init__(value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, '%d.%m.%Y')
            self.__value = new_value
        except ValueError:
            raise ValueError('Wrong data of birthday! Correct format: DD.MM.YYYY')       
    

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)if birthday else None
        self.phones = []
        if phone:
          self.phones.append(Phone(phone))          
          
    def add_phone(self, phone):
        if Phone(phone) not in self.phones:
            self.phones.append(Phone(phone))
        
    def add_birthday(self, birthday):
        self.birthday = (Birthday(birthday))
        
    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]
        
    def remove_birthday(self):
        if self.birthday:
            self.birthday = None
        
    def edit_phone(self, old_phone: str, new_phone: str):
        if old_phone in [p.value for p in self.phones]:
            for phone in self.phones:           
                if phone.value == old_phone:
                    self.phones.remove(phone)
                    self.phones.append(Phone(new_phone))
        else:
            raise ValueError            
        
    def find_phone(self, phone):
        for p in self.phones:            
            if p.value == phone:
                return p        
        return None
    
    def days_to_birthday(self):
        if self.birthday:
            current_date = datetime.today()
            birthday_date = datetime.strptime(self.birthday.value, '%d.%m.%Y').replace(year=current_date.year)
            if birthday_date < current_date:
                birthday_date = birthday_date.replace(year=current_date.year + 1)
            days_to_birthday = (birthday_date.date()- current_date.date()).days
            return days_to_birthday

    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday} and {Record.days_to_birthday(self)} days left until the next!"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        
        
class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
        
    def write_contacts_to_file(self, filename = "contacts.pkl"):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)            

    def read_contacts_from_file(self, filename = "contacts.pkl"):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
                print('Contacts uploaded successfully!')         
        except FileNotFoundError:
            print('AdressBook is empty!') 
        
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        self.write_contacts_to_file()   

    def delete(self, name):
        if self.data.pop(name, None):
            self.write_contacts_to_file()

    def find(self, name):
        return self.data.get(name)    
       
    def find_contacts(self, search):
        found_contacts = []
        if not len(search):
            return None
        for record in self.data.values():
            if (search.lower() in record.name.value.lower()): 
                found_contacts.append(record)
            for phone in record.phones:
                if search in phone.value:
                    found_contacts.append(record)
        if found_contacts:
            for r in found_contacts:
                print(r)
        else:
            print(f"Not found contacts with: {search}. Try again.")
        # return found_contacts
        
    def iterator(self, limit:int=1):
        for i in range(0, len(self.data), limit):
            if i <= len(self.data):
                result = list(self.data.values())[i:i+limit:]                    
                yield '\n'.join(str(record) for record in result)       
            else:
                raise StopIteration
            
    def __repr__(self):
        return str(self.value)
    
    def __str__(self):
       return  '\n'.join(str(record) for record in self.data.values())
   
   
if __name__ == "__main__":
    book = AddressBook()    
    book.read_contacts_from_file()
    
    # book.find_contacts('jo')
    # oleg_record = Record("Oleg")
    # oleg_record.add_phone("0135433568")
    # oleg_record.add_birthday("12.12.1970")
    # book.add_record(oleg_record)
    # book.delete('Bob')
    # book.find_contacts('4')
    