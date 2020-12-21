# -*- coding: utf-8 -*-

from django.core import mail
from django.utils import timezone
from django.test import TestCase as TestCaseBase
from django.conf import settings

from faker import Factory
from doubles import verify, teardown
from faker.providers import misc, profile

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase as BaseAPITestCase
from rest_framework_api_key.models import APIKey
from rest_framework.authtoken.models import Token

from accounts.tests.factories.user import UserFactory
from accounts.views import SigninAPIView
from accounts.auth import create_token

fake = Factory.create()
fake.add_provider(profile)
fake.add_provider(misc)


def mail_outbox():
    return len(mail.outbox)


def generate_profile():
    user_profile = fake.simple_profile()
    user_password = fake.uuid4()
    full_name = fake.name().split(" ")
    return {
        'username': user_profile['username'],
        'email': user_profile['mail'],
        'first_name': full_name[0],
        'last_name': full_name[1],
        'password': user_password,
    }


def generate_simple_profile():
    user_profile = fake.simple_profile()
    return {
        'id': user_profile['username'],
        'name': fake.name(),
        'email': user_profile['mail'],
    }


class TestDoublesMixin(TestCaseBase):
    def tearDown(self):
        super().tearDown()
        verify()
        teardown()


class TestUtilsMixin(TestCaseBase):
    TEST_EMAIL = 'test_user@mail.com'
    TEST_USERNAME = 'test_user'

    def setUp(self):
        super(TestUtilsMixin, self).setUp()
        self.user = UserFactory()
        self.user.save()


class APITestCase(TestUtilsMixin, BaseAPITestCase):

    api_url = None

    def generate_user(self, is_active=True):
        user = UserFactory(name=self.TEST_USERNAME, email=self.TEST_EMAIL)
        user.isActive = is_active
        user.save()
        return user

    def setUp(self):
        super(APITestCase, self).setUp()

        self.token = create_token(user=self.user)
        self.client = APIClient()
        self.auth_client = APIClient()
        self.failed_client = APIClient()

        self.auth_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.failed_client.credentials(HTTP_AUTHORIZATION='Token anything')

        self.current_local_hour = timezone.localtime(timezone.now()).hour
        settings.MARKET_OPEN_HOUR = self.current_local_hour - 1
        settings.MARKET_CLOSE_HOUR = self.current_local_hour + 1

    def swith_user(self, user):
        self.token, created = Token.objects.get_or_create(user=user)
        self.auth_client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def get(self, url=None, data=None, is_authenticated=False,
            use_api_key=False, **extra):
        if is_authenticated:
            self._attach_api_key_header(use_api_key)
            return self.auth_client.get(path=url, data=data, **extra)
        return self.client.get(path=url, data=data, **extra)

    def put(self, url=None, data=None, is_authenticated=False,
            use_api_key=False, **extra):
        if is_authenticated:
            self._attach_api_key_header(use_api_key)
            return self.auth_client.put(path=url, data=data, **extra)
        return self.client.put(path=url, data=data, **extra)

    def delete(self, url=None, data=None, is_authenticated=False,
            use_api_key=False, **extra):
        if is_authenticated:
            self._attach_api_key_header(use_api_key)
            return self.auth_client.delete(path=url, data=data, **extra)
        return self.client.delete(path=url, data=data, **extra)

    def get_failed(self, url=None, data=None, **extra):
        return self.failed_client.get(path=url, data=data, **extra)

    def post_failed(self, url=None, data=None, headers=None):
        headers = headers or {}
        return self.failed_client.post(path=url, data=data, **headers)

    def put_failed(self, url=None, data=None, **extra):
        return self.failed_client.put(path=url, data=data, **extra)

    def delete_failed(self, url=None, data=None, **extra):
        return self.failed_client.delete(path=url, data=data, **extra)

    def _attach_api_key_header(self, use_api_key=False):
        if use_api_key:
            api_key, key = APIKey.objects.create_key(name="generated-api-key")
            self.auth_client.credentials(
                HTTP_AUTHORIZATION='Api-Key {0}'.format(key),
            )

    @classmethod
    def _make_request_kwargs(cls, path, data, format, content_type):
        return {'path': path, 'data': data, 'format': format, 'content_type': content_type}

    def options(self, url=None, data=None, format=None, content_type=None,
                is_authenticated=False, use_api_key=False, **extra):

        kwargs = self._make_request_kwargs(url, data, format, content_type)
        if is_authenticated:
            self._attach_api_key_header(use_api_key)
            return self.auth_client.options(**kwargs, **extra)
        return self.client.options(**kwargs, **extra)

    def options_failed(self, url=None, data=None, headers=None):
        headers = headers or {}
        return self.failed_client.options(path=url, data=data, **headers)

    def post(self, url=None, data=None, format=None, content_type=None,
             is_authenticated=False, use_api_key=False, **params):

        kwargs = self._make_request_kwargs(url, data, format, content_type)
        if is_authenticated:
            self._attach_api_key_header(use_api_key)
            return self.auth_client.post(**kwargs, **params)
        return self.client.post(**kwargs, **params)

    def get_response_as_dict(self, response):
         return response if isinstance(response, dict) else response.json()

    def assertFormattedResponse(self, response):
        _response = self.get_response_as_dict(response)
        self.assertIn("detail", _response)


    def assertCode(self, response, detail):
        _response = self.get_response_as_dict(response)
        self.assertIn("detail", _response)
        if isinstance(detail, str):
            self.assertEqual(_response["detail"], detail)
        else:
            self.assertEqual(_response["detail"], detail["detail"])

    def assertBadRequest(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertUnauthorized(self, response):
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertForbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertNotFound(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertOk(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def assertNotContent(self, response):
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def assertCreated(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Authentication Asserts
    def assertNotAuthenticated(self, response):
        self.assertUnauthorized(response)
        self.assertFormattedResponse(response)
        self.assertCode(response, "Authentication credentials were not provided.")

    def assertAuthenticationFailed(self, response):
        self.assertUnauthorized(response)
        self.assertFormattedResponse(response)
        self.assertCode(response, "Invalid token.")

    def assertAuthenticatedGET(self, url, data=None):
        response = self.get(url, data, is_authenticated=False)
        self.assertNotAuthenticated(response)
        response = self.get_failed(url, data)
        self.assertAuthenticationFailed(response)

    def assertAuthenticatedPOST(self, url, data=None):
        response = self.post(url, data, is_authenticated=False)
        self.assertNotAuthenticated(response)
        response = self.post_failed(url, data)
        self.assertAuthenticationFailed(response)

    def assertAuthenticatedPUT(self, url, data=None):
        response = self.put(url, data, is_authenticated=False)
        self.assertNotAuthenticated(response)
        response = self.put_failed(url, data)
        self.assertAuthenticationFailed(response)

    def assertAuthenticatedDELETE(self, url, data=None):
        response = self.delete(url, data, is_authenticated=False)
        self.assertNotAuthenticated(response)
        response = self.delete_failed(url, data)
        self.assertAuthenticationFailed(response)

    def assertAuthenticatedOPTIONS(self, url, data=None):
        response = self.options(url, data, is_authenticated=False)
        self.assertNotAuthenticated(response)
        response = self.get_failed(url, data)
        self.assertAuthenticationFailed(response)


class TestCase(TestUtilsMixin):
    pass
