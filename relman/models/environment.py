from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy as _p

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
    product = models.ForeignKey(
        'Product',
        verbose_name=(_("Product"))
    )
    promotes_to = models.ForeignKey(
        'Environment',
        verbose_name=(_("Promotes to")),
        null=True,
        blank=True
    )

    def __unicode__(self):
        return u'%s: %s' % (self.product, self.name)

    class Meta:
        app_label = 'relman'
        unique_together = ('product', 'name'),


class Promotion(TimeStampedModel):
    """
    A promotion is a build within a an environment.
    """
    build = models.ForeignKey(
        'relman.Build',
        verbose_name=(_("Build")),
        editable=False
    )
    environment = models.ForeignKey(
        'Environment',
        verbose_name=(_("Environment")),
    )

    notes = models.TextField(_("Notes"), blank=True)

    def __unicode__(self):
        return u'%s [%s]' % (self.build, self.environment)

    class Meta:
        app_label = 'relman'
