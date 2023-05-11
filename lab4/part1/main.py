# strings --------------------------------------------------------------------------------------------------------------
def conc():
    print('\nКонкатенація --------------------------------------------------------------------------------------------')
    str1 = 'Hello'
    str2 = 'World'
    print(str1 + ' ' + str2)


def explode_implode():
    print('\nExplode implode -----------------------------------------------------------------------------------------')
    string = '1 2 3 4 5 6 7 8'
    splitted = string.split()
    print(f'"{string}" explode: {splitted}')
    print(f'{splitted} implode with ",": ' + ','.join(splitted))


def strings():
    print('\nРобота з рядками ----------------------------------------------------------------------------------------')
    conc()
    explode_implode()


# Hash arrays ----------------------------------------------------------------------------------------------------------
def hash_array():
    print('\nХеш масиви ----------------------------------------------------------------------------------------------')
    arr = {'Ann': 'cat', 'John': 'dog', 'Jane': 'parrot', 'Jake': 'fish'}
    for key in arr:
        print(f'{key} has a {arr[key]}')


# Singleton ------------------------------------------------------------------------------------------------------------
class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(metaclass=MetaSingleton):
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

    def show(self):
        print(self.name + ' ' + self.surname)


def singleton():
    print('\nSingleton -----------------------------------------------------------------------------------------------')
    cls1 = Singleton('name1', 'surname1')
    cls2 = Singleton('name2', 'surname2')
    cls1.show()
    cls2.show()


# OOP ------------------------------------------------------------------------------------------------------------------
class Human:
    def __init__(self, name, surname, age):
        self.name = name
        self.surname = surname
        self.age = age


class Student(Human):
    def __init__(self, name, surname, age, group):
        super().__init__(name, surname, age)
        self.group = group

    def __str__(self):
        return f'{self.surname} {self.name}\n{self.age} years old\nGroup: {self.group}'


def oop():
    print('\nOOP -----------------------------------------------------------------------------------------------------')
    student = Student('name', 'surname', 18, 'TV-13')
    print(student)


def main():
    strings()
    hash_array()
    singleton()
    oop()


if __name__ == '__main__':
    main()
