# -*- coding: utf-8 -*-

import factory
from faker import Factory

from vans.models import Status

fake = Factory.create()


class StatusFactory(factory.DjangoModelFactory):

	code = factory.LazyFunction(fake.word)
	name = factory.LazyFunction(fake.word)

	class Meta:
		model = Status