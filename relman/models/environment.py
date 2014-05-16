from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy as _p

from model_utils import Choices
from model_utils.models import TimeStampedModel


class Environment(models.Model):
    """
    An environment is a place where a build happens. If a build is successful
    in one environment, it is promoted to the next environment. If there is
    no next environment, then the build is successful.
    """
    name = models.CharField(
        _p("object name", "Name"),
        max_length=255
    )
    display_order = models.PositiveIntegerField(_("Display order"), default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'relman'
        ordering = ('display_order', 'name')


class Promotion(TimeStampedModel):
    """
    A promotion is a build within a an environment.
    """
    STATUS_CHOICES = Choices(
        ('awaiting', _("Awaiting")),
        ('failure', _("Failure")),
        ('success', _("Success")),
    )

    build = models.ForeignKey(
        'relman.Build',
        verbose_name=(_("Build")),
        related_name='promotions',
        editable=False
    )
    environment = models.ForeignKey(
        'Environment',
        verbose_name=(_("Environment")),
    )

    status = models.CharField(
        _("Status"),
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.awaiting
    )

    notes = models.TextField(_("Notes"), blank=True)

    @property
    def is_successful(self):
        return self.status == self.STATUS_CHOICES.success

    @property
    def is_unsuccessful(self):
        return self.status == self.STATUS_CHOICES.failure

    def __unicode__(self):
        return u'%s [%s]' % (self.build, self.environment)

    class Meta:
        app_label = 'relman'
