from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.handlers.wsgi import WSGIRequest
import json

from django.views.decorators.csrf import csrf_exempt


def index(request: WSGIRequest):
    if request.method == "GET":
        if not request.GET.get('page', ''):
            return redirect('http://127.0.0.1:8000/main/?page=landing')
        try:
            file = 'main/' + request.GET.get('page', '') + '.html'
            return render(request, file)
        except Exception as exc:
            return HttpResponse('<p style="text-align: center; font-size: 32px">Сторінки "' +
                                str(exc) + '" не існує</p>')
    if request.method == "POST":
        if request.GET.get('page', '') == 'signup':
            return signup(request)
        elif request.GET.get('page', '') == 'login':
            return login(request)


@csrf_exempt
def signup(request: WSGIRequest):
    with open('users.json', 'r') as json_file:
        users = json.load(json_file)
        if users:
            for user in users:
                if user == request.POST['email']:
                    return HttpResponse('<p style="text-align: center; font-size: 32px">" \
                                        Користувач з таким логіном уже зареєстрований</p>')
    with open('users.json', 'w') as json_file:
        users[request.POST['email']] = request.POST['password']
        json.dump(users, json_file)
    return redirect("http://127.0.0.1:8000/main/?page=login")


@csrf_exempt
def login(request: WSGIRequest):
    with open('users.json', 'r') as json_file:
        users = json.load(json_file)
    for email in users:
        if email == request.POST['email']:
            if users[email] == request.POST['password']:
                return redirect('http://127.0.0.1:8000/main/?page=landing')
            else:
                return HttpResponse('<p style="text-align: center; font-size: 32px">Неправильний пароль</p>')
    return HttpResponse('<p style="text-align: center; font-size: 32px">Користувача з таким логіном не існує</p>')
