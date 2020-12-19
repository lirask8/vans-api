# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_api_key.permissions import HasAPIKey

from vans.models import Van
from vans.api.v1.serializers import VanSerializer, CreateVanSerializer
from vans.services.van_services import VanService
from common.utils import get_object_or_none


class VansView(APIView):
    """Process the Van requests."""

    permission_classes = [IsAuthenticated | HasAPIKey]

    def get(self, request):
        """Get all vans.

        GET /api/v1/vans/
        """

        vans = Van.objects.all()

        serializer = VanSerializer(vans, many=True)

        return Response(serializer.data)

    def post(self, request):
    	"""Create a van.

    	POST /api/v1/vans/
    	"""

    	serializer = CreateVanSerializer(data=request.data, context={'request': request})

    	if serializer.is_valid():
    		van = VanService.create(serializer.validated_data, request.user)
    		created_van_serializer = VanSerializer(van)
    		return Response(created_van_serializer.data, status=status.HTTP_201_CREATED)
    	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VansDetailView(APIView):
	"""Process the Van detail request."""

	permission_classes = [IsAuthenticated | HasAPIKey]

	def get(self, request, uuid):
		"""Gets the van detail.

		GET /api/v1/vans/{uuid}/
		"""

		van = get_object_or_none(Van, id=uuid)
		if van:
			serializer = VanSerializer(van)
			return Response(serializer.data)
		else:
			message = {"error":"Van Not Found"} 
			return Response(message, status=status.HTTP_404_NOT_FOUND)