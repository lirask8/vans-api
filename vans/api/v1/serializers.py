# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import Serializer

from vans.models import Van
from vans.choices import EconomicTypes


class VanSerializer(serializers.ModelSerializer):
    """Helps to print the Van info."""

    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.status.name

    class Meta:
        model = Van
        fields = (
            'id',
            'plates',
            'economic_number',
            'seats',
            'status',
        )


class CreateVanSerializer(Serializer):
    """Helps to validate the Van data"""

    plates = serializers.RegexField(regex=r'^[A-Z0-9]{3}-[0-9]{3}$',required=True)
    economic_number = serializers.ChoiceField(choices=EconomicTypes.choices(), required=True)
    seats = serializers.IntegerField(required=True, min_value=1, max_value=25)
    status = serializers.CharField(required=True)


class UpdateVanSerializer(Serializer):
    """Helps to validate the Van data"""

    plates = serializers.RegexField(regex=r'^[A-Z0-9]{3}-[0-9]{3}$',required=True)
    seats = serializers.IntegerField(required=True, min_value=1, max_value=25)
    status = serializers.CharField(required=True)