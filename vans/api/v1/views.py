# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_api_key.permissions import HasAPIKey

from vans.models import Van
from vans.api.v1.serializers import VanSerializer


class VansView(APIView):
    """Process the Van requests."""

    permission_classes = [IsAuthenticated | HasAPIKey]

    def get(self, request):
        """Get vans.

        GET /api/v1/vans/
        """

        vans = Van.objects.all()

        serializer = VanSerializer(vans, many=True)

        return Response(serializer.data)