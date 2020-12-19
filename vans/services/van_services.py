# -*- coding: utf-8 -*-

from django.utils import timezone
from django.conf import settings

from dateutil.relativedelta import relativedelta

from rest_framework import serializers

from vans.models import Van, Status, Log
from common.utils import get_object_or_none

class VanService:
    """Contains utility methods to help van processes."""

    @classmethod
    def create(cls, van_data, user):
        """Register and validate a Van."""
        van_plates = van_data['plates']
        van_economic_number_prefix = van_data['economic_number']
        van_seats = van_data['seats']
        van_status = van_data['status']

        cls._validate_plates(van_plates)
        status = cls._validate_status(van_status)
        next_economic_number = cls._get_next_economic_number(van_economic_number_prefix)

        van = Van(
            plates=van_plates,
            eco_num_prefix=van_economic_number_prefix,
            eco_num_number=next_economic_number,
            seats=van_seats,
            status=status,
            created_by=user,
        )
        van.save()
        cls.log_event(user, van, None, status)
        return van

    @classmethod
    def update(cls, van_data, van, user):
        """Update a Van."""
        van_plates = van_data['plates']
        van_seats = van_data['seats']
        van_status = van_data['status']
        initial_status = van.status
        #TODO: update economic_number by PATCH to preserve idempotency

        if van.plates != van_plates:
            cls._validate_plates(van_plates)

        status = cls._validate_status(van_status)

        van.plates=van_plates
        van.seats=van_seats
        van.status=status
        van.save()

        cls.log_event(user, van, initial_status, status)

        return van

    @classmethod
    def _validate_plates(cls, plates):
        """Validate Van's plates are unique."""
        if get_object_or_none(Van, plates=plates):
            raise serializers.ValidationError('Plates in use by another van.')

    @classmethod
    def _validate_status(cls, van_status):
        """Validate Van's status."""
        status = get_object_or_none(Status, code=van_status)
        if status:
            return status
        else:
            raise serializers.ValidationError("Status doesn't exists.")


    @classmethod
    def _get_next_economic_number(cls, van_economic_number_prefix):
        """Gets the next economic number for this prefix"""
        van = Van.objects.filter(eco_num_prefix=van_economic_number_prefix).order_by('eco_num_number').last()
        #import ipdb; ipdb.set_trace()
        if van:
            return van.eco_num_number + 1
        else:
            return 1

    @classmethod
    def log_event(cls, user, van, initial_status, final_status):
        log = Log(
            user=user,
            van=van,
            initial_status=initial_status,
            final_status=final_status,
        )
        log.save()