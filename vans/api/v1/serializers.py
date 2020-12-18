# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import Serializer

from vans.models import Van


class VanSerializer(serializers.ModelSerializer):
    """Helps to print the van info."""

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