# -*- coding: utf-8 -*-

import pytest

from django.urls import reverse
from django.conf import settings

from vans.models import Van
from vans.choices import EconomicTypes
from common.tests.unit_tests import APITestCase, TestDoublesMixin
from vans.tests.factories.van import VanFactory
from vans.tests.factories.status import StatusFactory
from vans.tests.factories.log import LogFactory


@pytest.mark.django_db
class VansTests(TestDoublesMixin, APITestCase):

    @classmethod
    def make_request_url_vans(cls):
        return reverse('api:v1:vans')

    @classmethod
    def register_van_payload(cls, plates="AW3-150", economic_number="A1", seats=4, status="01"):
        return {
            "plates": plates,
            "economic_number": economic_number, 
            "seats": seats, 
            "status": status
        }

    def test_get_vans_credentials_required(self):
        request_url = self.make_request_url_vans()
        self.assertAuthenticatedGET(request_url)

    