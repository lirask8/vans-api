import os
import binascii
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from common.models import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    lastName = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    isActive = models.BooleanField(null=False, default=True)

    def is_authenticated(self):
        return True

    def makepassword(self):
        self.password = make_password(self.password)

    def save(self, *args, **kwargs):
        if self.password.find('pbkdf2_sha256$') == -1 and len(self.password) != 77:
            self.makepassword()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class RecoveryToken(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=False, blank=False)
    key = models.CharField(max_length=60, null=True, blank=True)
    expiration = models.DateTimeField(null=True, blank=True)
    expired = models.BooleanField(null=False, default=False)

    def makeToken(self):

        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):

        if not self.key:
            self.key = self.makeToken()
        if not self.expiration:
            self.expiration = timezone.now()
            self.expiration += timedelta(minutes=45)
        super(RecoveryToken, self).save(*args, **kwargs)

    def __str__(self):

        return self.key

    class Meta:

        verbose_name = _('Recovery token')
        verbose_name_plural = _('Recovery tokens')