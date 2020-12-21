# -*- coding: utf-8 -*-

import factory
from faker import Factory

from vans.choices import EconomicTypes
from vans.models import Van
from vans.tests.factories.status import StatusFactory
from accounts.tests.factories.user import UserFactory

fake = Factory.create()


class VanFactory(factory.DjangoModelFactory):

	plates = 'AAA-000'
	eco_num_prefix = EconomicTypes.A1
	eco_num_number = 1
	seats = 11
	status = factory.SubFactory(StatusFactory)
	created_by = factory.SubFactory(UserFactory)

	class Meta:
		model = Van