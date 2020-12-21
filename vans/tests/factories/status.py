# -*- coding: utf-8 -*-

import factory
import factory.fuzzy
from faker import Factory

from vans.models import Status

fake = Factory.create()


class StatusFactory(factory.DjangoModelFactory):

	code = factory.fuzzy.FuzzyText(length=2)
	name = factory.LazyFunction(fake.word)

	class Meta:
		model = Status