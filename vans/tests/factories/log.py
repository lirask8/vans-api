# -*- coding: utf-8 -*-

import factory
from faker import Factory

from vans.models import Log
from vans.tests.factories.status import StatusFactory
from vans.tests.factories.van import VanFactory
from accounts.tests.factories.user import UserFactory

fake = Factory.create()


class LogFactory(factory.DjangoModelFactory):

	user = factory.SubFactory(UserFactory)
	van = factory.SubFactory(VanFactory)
	initial_status = factory.SubFactory(StatusFactory)
	final_status = factory.SubFactory(StatusFactory)

	class Meta:
		model = Log