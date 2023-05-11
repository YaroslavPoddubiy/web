from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from . import models
import json


def landing(request):
    return render(request, 'main/landing.html')


def container(request):
    item_for = request.GET.get('for', '')
    item_group = request.GET.get('group', '')
    item_type = request.GET.get('type', '')
    with open('items.json', 'r', encoding='UTF-8') as json_file:
        items = json.load(json_file)
        items_len = len(items)
        i = 0
        while i < items_len:
            if item_for and items[i]['for'] != item_for or item_group and items[i]['group'] != item_group or \
               item_type and items[i]['type'] != item_type:
                items.remove(items[i])
                i -= 1
                items_len -= 1
            i += 1

        for i in range(len(items)):
            items[i] = models.Item(items[i]['id'], items[i]['name'], items[i]['price'],
                                   items[i]['description'], items[i]['characteristics'])
    return render(request, 'main/container.html', {'items': items})


def info(request):
    id = int(request.GET.get('id', 0))
    if id == 0:
        return HttpResponse('<p style="text-align: center; font-size: 32px">'
                            'Сторінка не знайдена. Вкажіть параметр "id"</p>')
    with open('items.json', 'r', encoding='UTF-8') as json_file:
        items = json.load(json_file)
        similar_items = []
        for item in items:
            if item['id'] == id:
                for i in items:
                    if item['characteristics']['Тип'] == i['characteristics']["Тип"] and item["id"] != i["id"]:
                        similar_items.append(models.Item(i['id'], i['name'], i['price'],
                                                         i['description'], i['characteristics']))
                return render(request, 'main/info.html',
                              {'item': models.Item(item['id'], item['name'], item['price'],
                                                   item['description'], item['characteristics']),
                               'similar_items': similar_items})
        return HttpResponse('<p style="text-align: center; font-size: 32px">'
                            'Товару з таким id не існує</p>')


@csrf_exempt
def signup(request: WSGIRequest):
    if request.method == "GET":
        return render(request, 'main/signup.html')
    elif request.method == "POST":
        with open('users.json', 'r') as json_file:
            users = json.load(json_file)
            if users:
                for user in users:
                    if user == request.POST['email']:
                        return HttpResponse("<p>Користувач з таким логіном уже зареєстрований</p>")
        with open('users.json', 'w') as json_file:
            users[request.POST['email']] = request.POST['password']
            json.dump(users, json_file)
    return redirect("http://127.0.0.1:8000/main/login")


@csrf_exempt
def login(request: WSGIRequest):
    if request.method == "GET":
        return render(request, 'main/login.html')
    elif request.method == "POST":
        with open('users.json', 'r') as json_file:
            users = json.load(json_file)
        for user in users:
            if user == request.POST['email']:
                if users[user] == request.POST['password']:
                    return redirect('http://127.0.0.1:8000/main/landing')
                else:
                    return HttpResponse("<p>Неправильний пароль</p>")
    return HttpResponse("<p>Користувача з таким логіном не існує</p>")
