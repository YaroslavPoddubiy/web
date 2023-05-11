from django.db import models

# Create your models here.


class Item:
    def __init__(self, id, name, price, description, characteristics):
        self.__id = id
        self.__name = name
        self.__price = price
        self.__description = description
        self.__keys = []
        self.__values = []
        self.__characteristics(characteristics)

    def __characteristics(self, characteristics):
        for key in characteristics:
            self.__keys.append(key)
            self.__values.append(characteristics[key])

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def description(self):
        return self.__description

    @property
    def keys(self):
        return self.__keys

    @property
    def values(self):
        return self.__values
