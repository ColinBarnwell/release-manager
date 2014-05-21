from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy as _p

from model_utils import Choices
from model_utils.models import TimeStampedModel

from mixins import CommentsMixin


class Checkpoint(models.Model):
    """
    A checkpoint is an environment, test suite or other item in a QA check list
    that a build can be checked against.
    """
    name = models.CharField(
        _p(u"object name", u"Name"),
        max_length=255
    )
    display_order = models.PositiveIntegerField(_("Display order"), default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'relman'
        ordering = ('display_order', 'name')


class Check(CommentsMixin, TimeStampedModel):
    """
    A check represents the testing of a single build against a single checkpoint.
    """
    STATUS_CHOICES = Choices(
        ('awaiting', _("Awaiting")),
        ('failure', _("Failure")),
        ('success', _("Success")),
    )

    build = models.ForeignKey(
        'relman.Build',
        verbose_name=(_("Build")),
        related_name='checks',
        editable=False
    )
    checkpoint = models.ForeignKey(
        'Checkpoint',
        verbose_name=(_("Checkpoint")),
    )

    status = models.CharField(
        _("Status"),
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.awaiting
    )

    @property
    def is_successful(self):
        return self.status == self.STATUS_CHOICES.success

    @property
    def is_unsuccessful(self):
        return self.status == self.STATUS_CHOICES.failure

    def get_absolute_url(self):
        return self.build.get_absolute_url()

    def __unicode__(self):
        return u'%s [%s]' % (self.build, self.checkpoint)

    class Meta:
        app_label = 'relman'
        unique_together = ('build', 'checkpoint'),
