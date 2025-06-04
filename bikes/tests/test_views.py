from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.order_url = reverse("order")
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration.html")

    def test_order_get(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order.html")

    def test_register_invalid_post_missing_fields(self):
        response = self.client.post(self.register_url, {
            "username": "",
            "email": "user@example.com",
            "password": "123456"
        })
        self.assertContains(response, "This field is required.", html=True)

    def test_register_invalid_post_invalid_email(self):
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "email": "invalid_email",
            "password": "123456"
        })
        self.assertContains(response, "Enter a valid email address.", html=True)

    def test_register_invalid_post_existing_username(self):
        response = self.client.post(self.register_url, {
            "username": "testuser",  # вже існує
            "email": "user2@example.com",
            "password": "123456"
        })
        self.assertContains(response, "A user with that username already exists.", html=True)

    def test_order_post_invalid_bike_type(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.order_url, {"bike_type": "unknown_type"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select a valid choice", html=False)

    def test_order_post_empty_form(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(self.order_url, {})
        self.assertContains(response, "This field is required.", html=True)

    def test_order_post_not_authenticated(self):
        response = self.client.post(self.order_url, {"bike_type": "electric"})
        self.assertEqual(response.status_code, 302)  # редірект на логін
        self.assertIn("/login", response.url)
