# -*- coding: utf-8 -*-

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_api_key.permissions import HasAPIKey

from vans.models import Van, Status
from vans.api.v1.serializers import VanSerializer, CreateVanSerializer, UpdateVanSerializer
from vans.services.van_services import VanService
from common.utils import get_object_or_none, response_with_error_404
from vans.services.van_services import VanService


class VansView(APIView):
    """Process the Van requests."""

    permission_classes = [IsAuthenticated | HasAPIKey]

    def get(self, request):
        """Get all vans.

        GET /api/v1/vans/
        """

        status_param = self.request.query_params.get('status', None)

        if status_param:
            vans = Van.objects.filter(status__code=status_param)
        else:
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


class VanView(APIView):
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
			return response_with_error_404()

	def put(self, request, uuid):
		"""Update a van.

		PUT /api/v1/vans/{uuid}/
		"""

		van = get_object_or_none(Van, id=uuid)
		if van:
			serializer = UpdateVanSerializer(data=request.data, context={'request': request})

			if serializer.is_valid():
				updated_van = VanService.update(serializer.validated_data, van, request.user)
				updated_van_serializer = VanSerializer(updated_van)
				return Response(updated_van_serializer.data, status=status.HTTP_200_OK)

			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return response_with_error_404()

	def delete(self, request, uuid):
		"""Deletes a van.

		DELETE /api/v1/vans/{uuid}/
		"""
		van = get_object_or_none(Van, id=uuid)
		if van:
			initial_status = van.status
			inactive_status = get_object_or_none(Status, code='04')
			van.status = inactive_status
			van.save()

			VanService.log_event(request.user, van, initial_status, inactive_status)

			return Response(status=status.HTTP_204_NO_CONTENT)
		else:
			return response_with_error_404()