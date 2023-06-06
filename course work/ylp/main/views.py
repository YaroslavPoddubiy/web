from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . import models
from datetime import date


def landing(request):
    return render(request, 'main/landing.html')


def container(request):
    items_for = [x.lower() for x in request.GET.get('for', '').split(';')]
    items_group = [x.lower() for x in request.GET.get('group', '').split(';')]
    items_type = [x.lower() for x in request.GET.get('type', '').split(';')]
    items_country = [x.lower() for x in request.GET.get('country', '').split(';')]
    price_from = request.GET.get('price-from', 0)
    price_to = request.GET.get('price-to', 0)
    sort = request.GET.get('sort', 'За рейтингом')
    if price_from:
        price_from = float(price_from)
    if price_to:
        price_to = float(price_to)
    items: list[models.Item] = list(models.Item.objects.all())
    items_len = len(items)
    i = 0
    while i < items_len:
        if (items_for[0] and items[i].characteristics.get(key="Призначення").value.lower() not in items_for) \
           or (items_group[0] and items[i].characteristics.get(key="Група").value.lower() not in items_group) \
           or (items_type[0] and items[i].characteristics.get(key="Тип").value.lower() not in items_type) or \
           (items_country[0] and items[i].characteristics.get(key="Країна-виробник").value.lower() not in items_country) \
           or price_from and items[i].price < price_from or price_to and items[i].price > price_to:
            items.remove(items[i])
            i -= 1
            items_len -= 1
        i += 1
    if sort.lower() == 'від дешевих до дорогих':
        items.sort(key=lambda x: x.price)
    if sort.lower() == 'від дорогих до дешевих':
        items.sort(key=lambda x: x.price, reverse=True)
    return render(request, 'main/container.html', {'items': items,
                                                   'types_url': items_type,
                                                   'group_url': items_group,
                                                   'for_url': items_for,
                                                   'countries_url': items_country,
                                                   'fors': models.Characteristic.objects.all().filter(key="Призначення"),
                                                   'groups': models.Characteristic.objects.all().filter(key="Група"),
                                                   'types': models.Characteristic.objects.all().filter(key="Тип"),
                                                   'countries': models.Characteristic.objects.all().filter(key="Країна-виробник"),
                                                   'sort': sort})


def info(request: WSGIRequest):
    id = int(request.GET.get('id', 0))
    if request.method == "POST":
        user = models.MyUser.objects.get(user=User.objects.get(username=request.user.username))
        models.Feedback.objects.create(text=request.POST.get('feedback', 'Немає тексту'), date=date.today(),
                                       user=user, item=models.Item.objects.get(id=id))
    view = request.GET.get('view', 'about')
    try:
        item = models.Item.objects.get(id=id)
    except Exception:
        return HttpResponse('<p style="text-align: center; font-size: 32px">'
                            'Товару з таким id не існує</p>')
    photo_index = int(request.GET.get('photo', 0))
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
                   'user': user,
                   'view': view,
                   'feedbacks': models.Feedback.objects.all().filter(item=models.Item.objects.get(id=id)),
                   'current_photo': list(item.photos)[photo_index]})


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
        return redirect(request.GET.get('next', '/main/landing'))


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
            user.user.username = username.strip()
            user.user.save()
        if first_name:
            user.user.first_name = first_name.strip()
            user.user.save()
        if last_name:
            user.user.last_name = last_name.strip()
            user.user.save()
        if email:
            user.user.email = email.strip()
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
    url = request.GET.get('next', "/main/cart")
    user: models.MyUser = models.MyUser.objects.get(user=User.objects.get(username=request.user.username))
    item = models.Item.objects.get(id=id)
    user.items.add(item)
    return redirect(url)


def del_from_cart(request: WSGIRequest):
    id = request.GET.get('id', 0)
    user: models.MyUser = models.MyUser.objects.get(user=User.objects.get(username=request.user.username))
    user.items.remove(models.Item.objects.get(id=int(id)))
    return redirect("http://127.0.0.1:8000/main/cart")


def del_feedback(request: WSGIRequest):
    models.Feedback.objects.get(id=request.GET.get('id', 100)).delete()
    return redirect(request.GET.get('next'))
