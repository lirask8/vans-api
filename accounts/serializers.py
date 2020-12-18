from rest_framework import serializers

#your serializers here

from accounts.models import (
	User,
)


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		exclude = (
			'created',
			'modified',
		)

class ProfileSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		exclude = (
			'created',
			'password',
			'isActive',
			'modified',
		)
