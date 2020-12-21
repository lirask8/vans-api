import base64
import os
import binascii
import uuid

import requests
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _

from rest_framework import status
from rest_framework.response import Response


class CommonMixin:

    @staticmethod
    def randomName(size=6):
        return binascii.hexlify(os.urandom(size)).decode()

    @staticmethod
    def uploadpath():

        today = timezone.now()

        abspath = "%d/%d/%d" % (today.year, today.month, today.day)

        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, abspath)):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, abspath))

        return abspath

    @staticmethod
    def getObjectOrNone(model=None, *args, **kwargs):

        try:
            entity = model.objects.get(*args, **kwargs)
        except model.DoesNotExist:

            entity = None

        return entity

    def returnSerializerErrors(self, dict={}):

        missingFields = []

        if not bool(dict):
            return False

        for k, v in dict.items():
            missingFields.append(k)

        fields = ', '.join(missingFields)

        return "%s %s" % (_("The following fields are required : "), fields)

    def sendEmail(self, subject, htmlContent, sender, to):

        email = EmailMessage(
            subject,
            htmlContent,
            sender,
            to=to
        )

        email.content_subtype = 'html'

        try:

            email.send(fail_silently=False)

            return True

        except email.SMTPException:

            return False


class ListableStrPropsMixin(object):
    """Mixin to process listable strings."""

    @classmethod
    def as_list(cls):
        """Returns a list from a key-value pair dict."""
        return [
            value for key, value in cls.__dict__.items()
            if isinstance(value, str) and not key.startswith('__')
        ]


def unique_id():
    """Generate unique id"""
    return base64.urlsafe_b64encode(uuid.uuid4(
        ).bytes).decode('utf-8').replace('==', '')


def get_object_or_none(model, *args, **kwargs):
    """Get object or none"""
    try:
        obj = model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        obj = None
    return obj


def pop_element(self, value, elements):
    index = 0
    for element in elements:
        if element == value:
            elements.pop(index)
            break
        index += 1


def update_element(new_value, elements):
    new_elements = ['pk']
    for element in new_value:
        new_elements.append(element)
    for old_element in elements:
        new_elements.append(old_element)
    new_list = list(new_elements)
    return tuple(new_list)

def response_with_error_404():
    message = {"error":"Van Not Found"} 
    return Response(message, status=status.HTTP_404_NOT_FOUND)