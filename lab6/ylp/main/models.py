from django.db import models
from django.contrib.auth.models import User as BaseUser


# Create your models here.


class Characteristic(models.Model):
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=40)

    objects = models.Manager()

    def __str__(self):
        return f'{self.key}: {self.value}'


class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.CharField(max_length=1000)
    characteristics = models.ManyToManyField(Characteristic)

    objects = models.Manager()

    @property
    def chars(self):
        return self.characteristics.all()

    @property
    def photos(self):
        images = [photo.image for photo in Image.objects.all().filter(item=self)]
        return images

    def __str__(self):
        return f'Name: {self.name}\nPrice: {self.price}\nDescription: {self.description}\nCharacteristics: ' + \
               '\n'.join(f'{char.key}: {char.value}' for char in self.characteristics.all())


class Image(models.Model):
    image = models.ImageField(upload_to='images/items/')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    objects = models.Manager()


class MyUser(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)

    objects = models.Manager()

    @property
    def cart(self):
        return self.items.all()
