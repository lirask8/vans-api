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

    ### Utils 

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

    ### GET vans

    def test_get_vans_credentials_required(self):
        request_url = self.make_request_url_vans()
        self.assertAuthenticatedGET(request_url)

    def test_get_vans(self):
        van = VanFactory()
        request_url = self.make_request_url_vans()
        response = self.get(
            request_url,
            is_authenticated=True,
            use_api_key=True
        )
        vans_json = response.json()

        self.assertOk(response)
        self.assertIsInstance(vans_json, list)
        self.assertEqual(len(vans_json), 1)
        van_response = vans_json[0]
        self.assertEqual(van_response['plates'], van.plates)

    ### POST van 

    def test_register_van_credentials_required(self):
        request_url = self.make_request_url_vans()
        self.assertAuthenticatedPOST(request_url)

    def test_register_van_parameters_missing(self):
        request_url = self.make_request_url_vans()
        response = self.post(
            url=request_url,
            data={},
            is_authenticated=True,
            use_api_key=True,
            content_type='application/json'
        )

        errors = response.json()
        self.assertBadRequest(response)
        self.assertEquals({'plates', 'economic_number', 'seats', 'status'}, set(errors.keys()))

    def test_register_van_invalid_plates_format(self):
        request_url = self.make_request_url_vans()
        response = self.post(
            url=request_url,
            data=self.register_van_payload(plates="AAAA"),
            is_authenticated=True,
            format='json',
        )

        errors = response.json()
        self.assertBadRequest(response)
        self.assertEquals('This value does not match the required pattern.', errors['plates'][0])

    def test_register_van_invalid_economic_number_choice(self):
        request_url = self.make_request_url_vans()
        response = self.post(
            url=request_url,
            data=self.register_van_payload(economic_number="G4"),
            is_authenticated=True,
            format='json',
        )

        errors = response.json()
        self.assertBadRequest(response)
        self.assertIn('is not a valid choice', errors['economic_number'][0])

    def test_register_van_duplicated_plates(self):
        request_url = self.make_request_url_vans()
        van = VanFactory()
        registered_plates = van.plates
        response = self.post(
            url=request_url,
            data=self.register_van_payload(plates=registered_plates),
            is_authenticated=True,
            format='json',
        )

        errors = response.json()
        self.assertBadRequest(response)
        self.assertIn('Plates in use by another van.', errors)

    def test_register_van_status_unknown(self):
        request_url = self.make_request_url_vans()
        response = self.post(
            url=request_url,
            data=self.register_van_payload(status="77"),
            is_authenticated=True,
            format='json',
        )

        errors = response.json()
        self.assertBadRequest(response)
        self.assertIn("Status doesn't exists.", errors)

    def test_register_van(self):
        request_url = self.make_request_url_vans()
        status = StatusFactory()
        response = self.post(
            url=request_url,
            data=self.register_van_payload(status=status.code),
            is_authenticated=True,
            format='json',
        )

        response_json = response.json()
        self.assertCreated(response)
        self.assertIsInstance(response_json, dict)
        self.assertIn('id', response_json)
        self.assertEquals(Van.objects.count(), 1)

    def test_register_van_validate_next_economic_number(self):
        request_url = self.make_request_url_vans()
        status = StatusFactory()
        van = VanFactory() #A1-0001
        response = self.post(
            url=request_url,
            data=self.register_van_payload(status=status.code),
            is_authenticated=True,
            format='json',
        )

        response_json = response.json()
        self.assertCreated(response)
        self.assertIsInstance(response_json, dict)
        self.assertIn('id', response_json)
        self.assertEquals(Van.objects.count(), 2)
        self.assertEquals(response_json['economic_number'], "A1-0002")

    