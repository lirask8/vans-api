# -*- coding: utf-8 -*-

import pytest

from django.test import TestCase

from vans.models import Van, Status
from vans.tests.factories.van import VanFactory
from vans.tests.factories.status import StatusFactory


from django.utils.translation import ugettext_lazy as _


@pytest.mark.django_db
class VanModelTests(TestCase):

    def test_string_representation(self):
        van = VanFactory()
        self.assertEqual(str(van), van.plates)

    def test_verbose_name(self):
        self.assertEqual(str(Van._meta.verbose_name),
                         _('Van'))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Van._meta.verbose_name_plural),
                         _('Vans'))


@pytest.mark.django_db
class StatusModelTests(TestCase):

    def test_string_representation(self):
        status = StatusFactory()
        self.assertEqual(str(status), status.name)

    def test_verbose_name(self):
        self.assertEqual(str(Status._meta.verbose_name),
                         _('Status'))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Status._meta.verbose_name_plural),
                         _('Status'))