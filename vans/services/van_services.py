# -*- coding: utf-8 -*-

from django.utils import timezone
from django.conf import settings

from dateutil.relativedelta import relativedelta

from rest_framework import serializers

from vans.models import Van, Status
from common.utils import get_object_or_none

class VanService:
    """Contains utility methods to help van processes."""

    @classmethod
    def create(cls, van_data, user):
        """Register and validate a van."""
        van_plates = van_data['plates']
        van_economic_number = van_data['economic_number']
        van_seats = van_data['seats']
        van_status = van_data['status']

        status = get_object_or_none(Status, code=van_data['status'])

        if status:
            
            van = Van(
                plates=van_plates,
                economic_number=van_economic_number,
                seats=van_seats,
                status=status,
                created_by=user,
            )
            van.save()
            
            return van
        else:
            raise serializers.ValidationError("Status doesn't exists.")

    @classmethod
    def _validate_plates(cls, plates):
        """Validate Van's plates."""
        pass

