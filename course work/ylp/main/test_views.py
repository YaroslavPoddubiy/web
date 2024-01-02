from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from . import models
from datetime import date
# Create your tests here.


class TestContainerView(TestCase):
    def setUp(self) -> None:
        self.characteristic_for = models.Characteristic.objects.create(key='Призначення', value='for test')
        self.characteristic_group = models.Characteristic.objects.create(key='Група', value='group test')
        self.characteristic_type = models.Characteristic.objects.create(key='Тип', value='type test')
        self.characteristic_country = models.Characteristic.objects.create(key='Країна-виробник', value='country test')

        self.item1: models.Item = models.Item.objects.create(name='Item 1', price=10)
        self.item1.characteristics.add(self.characteristic_for)
        self.item1.characteristics.add(self.characteristic_group)
        self.item1.characteristics.add(self.characteristic_type)
        self.item1.characteristics.add(self.characteristic_country)

        self.item2 = models.Item.objects.create(name='Item 2', price=20)
        self.item2.characteristics.add(self.characteristic_for)
        self.item2.characteristics.add(self.characteristic_group)
        self.item2.characteristics.add(self.characteristic_type)
        self.item2.characteristics.add(self.characteristic_country)

    def tearDown(self) -> None:
        pass

    def test_container_view_with_filters(self):
        url = reverse('main:container')

        data = {
            'for': self.characteristic_for.value,
            'group': self.characteristic_group.value,
            'type': self.characteristic_type.value,
            'country': self.characteristic_country.value,
            'price-from': 5,
            'price-to': 15
        }

        response = self.client.get(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item 1')
        self.assertNotContains(response, 'Item 2')

    def test_container_view_without_filters(self):
        url = reverse('main:container')

        response: HttpResponse = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')


class TestInfoView(TestCase):
    def setUp(self) -> None:
        self.characteristic_type1 = models.Characteristic.objects.create(key="Тип", value="value1")
        self.characteristic_type2 = models.Characteristic.objects.create(key="Тип", value="value2")
        self.item1 = models.Item.objects.create(name='Item 1', price=20, description='description')
        self.item1.characteristics.add(self.characteristic_type1)
        self.item2 = models.Item.objects.create(name="Item 2", price=50)
        self.item2.characteristics.add(self.characteristic_type1)
        self.item3 = models.Item.objects.create(name="Item 3", price=10)
        self.item3.characteristics.add(self.characteristic_type2)
        self.item4 = models.Item.objects.create(name="Item 4", price=100)

    def tearDown(self) -> None:
        pass

    def test_info_view_item_exists(self):
        url = reverse('main:info')

        response = self.client.get(url, {'id': self.item1.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item 1')

    def test_info_view_item_does_not_exist(self):
        url = reverse('main:info')

        response = self.client.get(url, {'id': self.item4.id + 1})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Item 1')

    def test_info_view_item_with_description_and_characteristics(self):
        url = reverse('main:info')

        response = self.client.get(url, {'id': self.item1.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item 1')
        self.assertGreater(str(response.content).count('characteristics'), 2)
        self.assertContains(response, 'description')

    def test_info_view_item_without_description_and_characteristics(self):
        url = reverse('main:info')

        response: HttpResponse = self.client.get(url, {'id': self.item4.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item 4')

        self.assertLess(str(response.content).count('characteristics'), 3)
        self.assertNotContains(response, 'description')

    def test_info_view_item_with_similar_items(self):
        url = reverse('main:info')

        response = self.client.get(url, {'id': self.item1.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'similars')
        self.assertContains(response, 'Item 2')

    def test_info_view_item_without_similar_items(self):
        url = reverse('main:info')

        response = self.client.get(url, {'id': self.item3.id})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item 3')
        self.assertNotContains(response, 'similars')

    def test_info_view_add_feedback(self):
        user = User.objects.create_user(username='email', password='password')
        self.existing_user = models.MyUser.objects.create(user=user)
        self.client.login(username='email', password='password')

        response = self.client.post(reverse('main:info'), {'id': self.item1.id, 'feedback': 'test feedback'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(models.Feedback.objects.all().filter(item=self.item1)), 1)


class TestSignUpView(TestCase):
    def setUp(self) -> None:
        user = User(username='email')
        user.set_password('password')
        user.save()
        self.existing_user = models.MyUser.objects.create(user=user)

    def test_signup_view_user_does_not_exist(self):
        url = reverse('main:signup')

        response: HttpResponse = self.client.post(url, {'email': 'email1',
                                                        'password': 'password1'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_signup_view_user_exists(self):
        url = reverse('main:signup')

        response: HttpResponse = self.client.post(url, {'email': self.existing_user.user.username,
                                                        'password': 'password1'})

        self.assertNotEqual(response.status_code, 302)


class TestSignInView(TestCase):
    def setUp(self) -> None:
        self.email = 'email'
        self.password = 'password'
        user = User(username=self.email)
        user.set_password(self.password)
        user.save()
        self.existing_user = models.MyUser.objects.create(user=user)

    def test_signup_view_user_does_not_exist(self):
        url = reverse('main:login')

        response: HttpResponse = self.client.post(url, {'email': 'email1',
                                                        'password': 'password1'})

        self.assertNotEqual(response.status_code, 302)

    def test_signup_view_exists(self):
        url = reverse('main:login')

        response: HttpResponse = self.client.post(url, {'email': self.email,
                                                        'password': self.password})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.existing_user.user.is_authenticated, True)


class TestProfileView(TestCase):
    def setUp(self) -> None:
        self.email = 'email'
        self.password = 'password'
        user = User.objects.create_user(username=self.email, password=self.password)
        self.existing_user = models.MyUser.objects.create(user=user)

    def test_profile_view_change_info(self):
        url = reverse('main:profile')

        self.client.login(username='email', password='password')

        data = {'first_name': 'first_name1',
                'last_name': 'last_name1',
                'email': 'email@gmail.com'}

        response = self.client.post(url, data)

        user = User.objects.get(username='email')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.first_name, 'first_name1')
        self.assertEqual(user.last_name, 'last_name1')
        self.assertEqual(user.email, 'email@gmail.com')


class TestCartView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='email', password='password')
        self.existing_user = models.MyUser.objects.create(user=user)

        self.existing_user.items.add(models.Item.objects.create(name="Item 1", price=20))

    def test_cart_view(self):
        self.client.login(username='email', password='password')
        url = reverse('main:cart')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Item 1")


class TestAddToCartView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='email', password='password')
        self.existing_user = models.MyUser.objects.create(user=user)
        self.item = models.Item.objects.create(name='Item 1', price=15)

    def test_add_to_cart_view(self):
        self.client.login(username='email', password='password')

        response = self.client.get(reverse('main:add_to_cart'), {'id': self.item.id})

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.item, self.existing_user.cart)


class TestDelFromCartView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='email', password='password')
        self.existing_user = models.MyUser.objects.create(user=user)
        self.item1 = models.Item.objects.create(name='Item 1', price=15)
        self.item2 = models.Item.objects.create(name='Item 2', price=25)
        self.existing_user.items.add(self.item1)
        self.existing_user.items.add(self.item2)

    def test_add_to_cart_view(self):
        self.client.login(username='email', password='password')

        response = self.client.get(reverse('main:del_from_cart'), {'id': self.item1.id})

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.item2, self.existing_user.cart)
        self.assertNotIn(self.item1, self.existing_user.cart)


class TestDelFeedbackView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='email', password='password')
        self.existing_user = models.MyUser.objects.create(user=user)
        self.item = models.Item.objects.create(name='Item 1', price=15)
        self.feedback = models.Feedback.objects.create(text='test text', date=date.today(),
                                                       user=self.existing_user, item=self.item)

    def test_del_feedback_view(self):
        url = reverse('main:del_feedback')
        response = self.client.get(url, {'id': self.feedback.id})

        try:
            feedback = models.Feedback.objects.get(id=self.feedback.id)
        except Exception:
            feedback = None
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(feedback)
