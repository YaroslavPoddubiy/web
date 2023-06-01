from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
import json


def landing(request):
    return render(request, 'main/landing.html')


def container(request):
    item_for = request.GET.get('for', '')
    item_group = request.GET.get('group', '')
    item_type = request.GET.get('type', '')
    items = list(models.Item.objects.all())
    items_len = len(items)
    i = 0
    while i < items_len:
        if item_for and items[i].chars.get(key="Призначення").value.lower() != item_for.lower() \
           or item_group and items[i].chars.get(key="Група").value.lower() != item_group.lower() or \
           item_type and items[i].chars.get(key="Тип").value.lower() != item_type.lower():
            items.remove(items[i])
            i -= 1
            items_len -= 1
        i += 1
    return render(request, 'main/container.html', {'items': items})


def info(request):
    id = int(request.GET.get('id', 0))
    try:
        item = models.Item.objects.get(id=id)
    except Exception:
        return HttpResponse('<p style="text-align: center; font-size: 32px">'
                            'Товару з таким id не існує</p>')
    type = item.chars.get(key='Тип').value
    similar_items = []
    for _item in models.Item.objects.all():
        if type == _item.chars.get(key='Тип').value and id != _item.id:
            similar_items.append(_item)
    try:
        user = models.MyUser.objects.get(user=User.objects.get(username=request.user.username))
    except Exception:
        user = None
    return render(request, 'main/info.html',
                  {'item': item,
                   'similar_items': similar_items,
                   'user': user})


@csrf_exempt
def signup(request: WSGIRequest):
    if request.method == "GET":
        return render(request, 'main/signup.html')
    elif request.method == "POST":
        user = User(username=request.POST['email'])
        user.set_password(request.POST['password'])
        user.save()
        models.MyUser.objects.create(user=user)
    return redirect("http://127.0.0.1:8000/main/login")


@csrf_exempt
def signin(request: WSGIRequest):
    if request.method == "GET":
        return render(request, 'main/login.html')
    elif request.method == "POST":
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        if not user:
            return HttpResponse('<p>Неправильно задані дані</p>')
        login(request, user)
        return redirect('http://127.0.0.1:8000/main/landing')


def signout(request: WSGIRequest):
    logout(request)
    return redirect("http://127.0.0.1:8000/main/landing")


def profile(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect("http://127.0.0.1:8000/main/login")
    user: models.MyUser = models.MyUser.objects.get(user=User.objects.get(username=request.user.username))
    if request.method == "GET":
        return render(request, 'main/profile.html', {'user': user})
    if request.method == "POST":
        username = request.POST.get('username', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        if username:
            user.user.username = username
            user.user.save()
        if first_name:
            user.user.first_name = first_name
            user.user.save()
        if last_name:
            user.user.last_name = last_name
            user.user.save()
        if email:
            user.user.email = email
            user.user.save()
        return render(request, 'main/profile.html', {'user': user})


def cart(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect("http://127.0.0.1:8000/main/login")
    user = models.MyUser.objects.get(user=User.objects.get(username=request.user.username))
    return render(request, 'main/cart.html', {'items': user.cart})


def add_to_cart(request: WSGIRequest):
    if not request.user.is_authenticated:
        return redirect("http://127.0.0.1:8000/main/login")
    id = int(request.GET.get('id', 1))
    user: models.MyUser = models.MyUser.objects.get(user=User.objects.get(username=request.user.username))
    item = models.Item.objects.get(id=id)
    user.items.add(item)
    return redirect("http://127.0.0.1:8000/main/cart")


def del_from_cart(request: WSGIRequest):
    id = request.GET.get('id', 0)
    user: models.MyUser = models.MyUser.objects.get(user=User.objects.get(username=request.user.username))
    user.items.remove(models.Item.objects.get(id=int(id)))
    return redirect("http://127.0.0.1:8000/main/cart")
