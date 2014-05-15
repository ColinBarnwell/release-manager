from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy as _p

from mixins import SoftwareVersion


class Package(models.Model):
    """
    A package is a software component that has its own version releases, and on
    which a product release may depend, but is not in itself a product and is
    only indirectly part of the release schedule.
    """
    name = models.CharField(
        _p("object name", "Name"),
        max_length=255,
        unique=True
    )

    def current_version(self):
        versions = self.versions.filter(
            status=PackageVersion.STATUS_CHOICES.released
        )[:1]
        if versions:
            return versions[0]

    def next_version(self):
        versions = self.versions.filter(
            status__in=(
                PackageVersion.STATUS_CHOICES.proposed,
                PackageVersion.STATUS_CHOICES.in_progress,
            )
        ).order_by('target_date')[:1]
        if versions:
            return versions[0]

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'relman'


class PackageVersion(SoftwareVersion):
    """
    A version of a package.
    """
    package = models.ForeignKey(
        Package,
        verbose_name=(_("Package")),
        related_name='versions',
        editable=False
    )
    previous_version = models.ForeignKey(
        'PackageVersion',
        verbose_name=(_("Previous version")),
        null=True,
        blank=True
    )

    def __unicode__(self):
        return super(PackageVersion, self).__unicode__(name=self.package.name)

    class Meta(SoftwareVersion.Meta):
        app_label = 'relman'
