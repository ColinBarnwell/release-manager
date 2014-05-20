from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy as _p

from model_utils import Choices

from mixins import CommentsMixin, SoftwareVersion


class Package(models.Model):
    """
    A package is a software component that has its own version releases, and on
    which a product release may depend, but is not in itself a product and is
    only indirectly part of the release schedule.
    """
    name = models.CharField(
        _p(u"object name", u"Name"),
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

    def get_absolute_url(self):
        return reverse('package_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'relman'


class PackageVersion(CommentsMixin, SoftwareVersion):
    """
    A version of a package.
    """
    package = models.ForeignKey(
        Package,
        verbose_name=(_("Package")),
        related_name='versions',
        editable=False
    )

    def previous_versions(self):
        return PackageVersion.objects.filter(
            package=self.package
        ).filter(
            models.Q(
                major_version=self.major_version,
                minor_version=self.minor_version,
                patch_version__lt=self.patch_version
            ) |
            models.Q(
                major_version=self.major_version,
                minor_version__lt=self.minor_version
            ) |
            models.Q(
                major_version__lt=self.major_version
            )
        )

    def get_absolute_url(self):
        return u"%s?v=%s" % (self.package.get_absolute_url(), self.version_number())

    def get_ajax_url(self):
        return reverse('version_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return super(PackageVersion, self).__unicode__(name=self.package.name)

    class Meta(SoftwareVersion.Meta):
        app_label = 'relman'


class PackageVersionBuild(CommentsMixin):
    """
    A package version build represents an iteration of the current release
    """
    STATUS_CHOICES = Choices(
        ('in_progress', _("In progress")),
        ('rejected', _("Rejected")),
        ('provisional', _("Provisional")),
        ('accepted', _("Accepted")),
    )

    version = models.ForeignKey(
        PackageVersion,
        verbose_name=(_("Version")),
        related_name='builds',
        editable=False
    )
    code = models.CharField(_("Code"), max_length=32)

    status = models.CharField(
        _("Status"),
        max_length=16,
        choices=STATUS_CHOICES
    )

    @property
    def is_accepted(self):
        return self.status == self.STATUS_CHOICES.accepted

    @property
    def is_provisional(self):
        return self.status == self.STATUS_CHOICES.provisional

    @property
    def is_rejected(self):
        return self.status == self.STATUS_CHOICES.rejected

    def get_absolute_url(self):
        return self.version.get_absolute_url()

    def __unicode__(self):
        return u"%s.%s" % (self.version.version_number(), self.code)

    class Meta:
        app_label = 'relman'
        ordering = '-code',
        unique_together = ('version', 'code')


class Change(CommentsMixin):
    """
    A change introduced by a new version.
    """
    version = models.ForeignKey(
        PackageVersion,
        verbose_name=(_("Version")),
        related_name='changes',
        editable=False
    )
    description = models.TextField(
        _("Description")
    )

    def __unicode__(self):
        return self.description

    class Meta:
        app_label = 'relman'
