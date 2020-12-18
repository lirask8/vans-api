# -*- coding: utf-8 -*-

import factory
from faker import Factory
from faker.providers import person, profile

from accounts.models import User

fake = Factory.create()
fake.add_provider(person)
fake.add_provider(profile)


def fake_username():
    return fake.simple_profile()["username"]


class UserFactory(factory.DjangoModelFactory):

    name = factory.LazyFunction(fake_username)
    email = factory.LazyFunction(fake.email)
    lastName = factory.LazyFunction(fake.first_name)
    secondLastName = factory.LazyFunction(fake.last_name)
    password = factory.LazyFunction(fake.word)
    cash = 100000

    class Meta:
        model = User
