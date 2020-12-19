from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _

from common.models import BaseModel
from vans.choices import EconomicTypes


class Van(BaseModel):
    """Represents the Van."""

    plates = models.CharField(
    	verbose_name=_('Plates'),
    	unique=True,
    	max_length=7,
    	blank=False, null=False,
    )

    eco_num_prefix = models.CharField(
    	verbose_name=_('Economic Number Prefix'),
    	choices=EconomicTypes.choices(),
    	max_length=2,
    	blank=False, null=False,
    )

    eco_num_number = models.PositiveIntegerField(
    	verbose_name=_('Economic Number Consecutive'),
    	blank=False, null=False,
    )

    seats = models.PositiveIntegerField(
    	verbose_name=_('Seats'),
    	validators=[MinValueValidator(1)],
    )

    status = models.ForeignKey(
    	'vans.Status',
    	verbose_name=_('Status'),
    	on_delete=models.PROTECT,
    	null=True, blank=True,
    )

    created_by = models.ForeignKey(
    	'accounts.User',
    	verbose_name=_('Created by'),
    	on_delete=models.PROTECT,
    	null=True, 
    )

    @property
    def economic_number(self):
        return self.eco_num_prefix + '-' + str(self.eco_num_number)

    def __str__(self):
        return self.plates

    class Meta:
        db_table = 'van'
        verbose_name = _('Van')
        verbose_name_plural = _('Vans')
        app_label = 'vans'


class Status(BaseModel):
	"""Represents the Van's Status."""

	code = models.CharField(
		verbose_name=_('Code'),
		max_length=10,
		unique=True,
		null=False,
		blank=False
	)

	name = models.CharField(
		verbose_name=('Status name'),
		max_length=50,
		null=False, blank=False
	)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'status'
		verbose_name = _('Status')
		verbose_name_plural = _('Status')
		app_label = 'vans'


class Log(BaseModel):
	"""Represents the Van's Log."""

	user = models.ForeignKey(
		'accounts.User',
		verbose_name=_('User'),
		on_delete=models.PROTECT,
		null=False, blank=False
	)

	van = models.ForeignKey(
		'vans.Van',
		verbose_name=_('Van'),
		on_delete=models.PROTECT,
		null=False, blank=False
	)

	initial_status = models.ForeignKey(
		'vans.Status',
		verbose_name=_('Initial Status'),
		on_delete=models.PROTECT, 
		null=True, blank=True, 
		related_name='initial'
	)

	final_status = models.ForeignKey(
		'vans.Status',
		verbose_name=_('Final Status'),
		on_delete=models.PROTECT,
		null=False, blank=False,
		related_name='final'
	)

	def __str__(self):
		return self.id

	class Meta:
		db_table = 'log'
		verbose_name = _('Log')
		verbose_name_plural = _('Logs')
		app_label = 'vans'