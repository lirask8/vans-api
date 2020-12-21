# -*- coding: utf-8 -*-

import jwt
import datetime

from django.conf import settings
from django.contrib.auth.hashers import check_password

from common.utils import CommonMixin
from accounts.models import User


def authenticate(email, password):

	user = CommonMixin.getObjectOrNone(User,email=email)
	if user and not check_password(password,user.password):
		return None
	return user


def create_token(user):
	token = jwt.encode({
		'sub': user.id,
		'iat': datetime.datetime.utcnow(),
		'exp': datetime.datetime.utcnow() + datetime.timedelta(days=364)
	},
		settings.SECRET_KEY
	).decode('utf-8')

	return token
