# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from common.utils import ListableStrPropsMixin


class EconomicTypes(ListableStrPropsMixin):
    """Define all the economic number (prefix) types"""

    A1 = 'A1'
    A2 = 'A2'
    A3 = 'A3'

    @classmethod
    def choices(cls):
        return (
            (cls.A1, _('A1')),
            (cls.A2, _('A2')),
            (cls.A3, _('A3')),
        )