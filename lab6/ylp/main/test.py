import requests
import json
# import models
from django.conf import settings


# settings.configure(DEBUG=True, TEMPLATE_DEBUG=True, INSTALLED_APPS=[
#     'main',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
# ])
    # TEMPLATE_DIRS=('/home/web-apps/myapp', '/home/web-apps/base'))


settings.configure(default_settings=a)


import models


def main():
    # # link = "http://127.0.0.1:8000/main/signup"
    # # # response = requests.get(link, {'page': 'landing'})
    # # # print(response.text)
    # # responce = requests.post(link, {'email': 'ypod12389', 'password': '12345'})
    # # print(responce.text)
    # response = requests.get('http://127.0.0.1:8000/main/', {'page': 'landing'})
    # print(response.text)
    with open('test.json', 'w') as file:
        pass
    # with open('items.json', 'r', encoding='utf-8') as file:
    #     items = json.load(file)
    #     for item in items:
    #         models.Item.objects.create(id=int(item['id']), name=item['name'], price=float(item['price']),
    #                                    description=item['description'])


if __name__ == '__main__':
    main()
