from django.db import models
from common.utils import get_object_or_none, unique_id


class BaseModel(models.Model):
    """Base model"""

    id = models.CharField(primary_key=True, max_length=22, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def make_id(self):
        uid = unique_id()[::2]
        obj = get_object_or_none(self.__class__, pk=uid)

        self.id = uid if not obj else ''

    def save(self, *args, **kwargs):
        while not self.id: self.make_id()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ('modified',)