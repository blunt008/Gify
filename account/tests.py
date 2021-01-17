from django.test import TestCase
from django.contrib.auth import get_user_model
from account.forms import UserRegistrationForm
from django.urls import reverse
from http import HTTPStatus

from .forms import UserRegistrationForm

class RegisterFormTests(TestCase):

    def setUp(self):
        get_user_model().objects.create(
            username="Damian",
            password="testaccount"
        )

    def test_username_taken(self):
        form = UserRegistrationForm(data={
            "username": "Damian",
            "password": "test",
            "password2": "test"
        })

        self.assertEqual(
            form.errors["username"],
            ["A user with that username already exists."]
        )

    def test_password_too_short(self):
        form = UserRegistrationForm(data={
            "username": "damian2",
            "password": "test",
            "password2": "test"
        })

        self.assertEqual(
            form.errors["password"],
            ["Password is too short. Min. 8 characters."]
        )
        
    def test_not_matching_passwords(self):
        form = UserRegistrationForm(data={
            "username": "damian2",
            "password": "testingaccount",
            "password2": "test"
        })

        self.assertEqual(
            form.errors["password2"],
            ["Passwords don't match."]
        )

class RegisterViewTests(TestCase):

    def test_get(self):
        response = self.client.get("/register/")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response,
            "<h1>Create an account</h1>",
            html=True
        )

    def test_post_success(self):
        response = self.client.post(
            "/register/",
            data={
                "username": "John",
                "avatar": "",
                "password": "testaccount",
                "password2": "testaccount"
            },
        )
    
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "account/register_done.html")
        self.assertEqual(
            get_user_model().objects.count(), 1
        )

    def test_post_error(self):
        response = self.client.post(
            "/register/",
            data={
                "username": "John",
                "password": "testing"
            }
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            "account/register.html"
        )

class LoginViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='Damianek',
            password='testpassword'
        )

    def test_user_exists(self):
        users = get_user_model().objects.count()
        self.assertEqual(users, 1)

    def test_redirect_to_login_page(self):
        response = self.client.get('/')

        self.assertRedirects(response, "/login/?next=/")

    def test_login_template_displayed(self):
        response = self.client.get('/', follow=True)

        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_failure(self):
        login = self.client.login(username='username', password='password')

        self.assertFalse(login)

    def test_login_succesfull(self):
        self.credentials = {
            'username': 'Damianek',
            'password': 'testpassword'
        }
        login = self.client.login(**self.credentials)

        self.assertTrue(login)
        

