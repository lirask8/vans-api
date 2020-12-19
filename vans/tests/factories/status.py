# -*- coding: utf-8 -*-

import factory
from faker import Factory

from vans.models import Status

fake = Factory.create()


class StatusFactory(factory.DjangoModelFactory):

	code = '01'
	name = 'status_name'

	class Meta:
		model = Status