from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy as _p

from model_utils import Choices

from mixins import CommentsMixin, SoftwareVersion


class Product(models.Model):
    """
    A product is a thing that gets released. It may be a simple application
    with no dependencies, or it might be a complex piece of software pulling
    together multiple packages, each with their own version numbers.
    """
    name = models.CharField(
        _p("object name", "Name"),
        max_length=255,
        unique=True
    )

    def current_release(self):
        releases = self.releases.filter(
            status=ProductRelease.STATUS_CHOICES.released
        )[:1]
        if releases:
            return releases[0]

    def current_release_version(self):
        current_release = self.current_release()
        if current_release:
            return current_release.version_number()
        return ''

    def next_release(self):
        releases = self.releases.filter(
            status__in=(
                ProductRelease.STATUS_CHOICES.proposed,
                ProductRelease.STATUS_CHOICES.in_progress,
            )
        ).order_by('target_date')[:1]
        if releases:
            return releases[0]

    def next_release_version(self):
        next_release = self.next_release()
        if next_release:
            return '%s (%s)' % (
                next_release.version_number(),
                next_release.get_status_display()
            )
        return ''

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'relman'


class ProductRelease(CommentsMixin, SoftwareVersion):
    """
    A release is an event, either in the past or in the future, that represents
    a product being deployed in a specific state.
    """
    product = models.ForeignKey(
        Product,
        verbose_name=(_("Product")),
        related_name='releases',
    )
    release_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Release manager"),
        null=True,
        blank=True
    )
    dependencies = models.ManyToManyField(
        'PackageVersion',
        verbose_name=(_("Dependencies")),
        related_name='dependants',
        null=True,
        blank=True
    )

    def previous_versions(self):
        return ProductRelease.objects.filter(
            product=self.product
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
        return u"%s?v=%s" % (self.product.get_absolute_url(), self.version_number())

    def get_delete_url(self):
        return reverse('release_delete', kwargs={'pk': self.pk})

    def get_ajax_url(self):
        return reverse('release_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return super(ProductRelease, self).__unicode__(name=self.product.name)

    class Meta(SoftwareVersion.Meta):
        app_label = 'relman'


class Build(CommentsMixin):
    """
    A build represents a deployment of a release version. A successful build
    is a successful release. An unsuccessful build should be superceded by a
    new build, once code or environment changes have been made.
    """
    STATUS_CHOICES = Choices(
        ('scheduled', _("Scheduled")),
        ('in_progress', _("In progress")),
        ('failed', _("Failed")),
        ('successful', _("Successful")),
    )

    release = models.ForeignKey(
        ProductRelease,
        verbose_name=(_("Release")),
        related_name='builds'
    )

    build_number = models.PositiveIntegerField(default=1)
    code_name = models.CharField(_("Code name"), max_length=32, blank=True)

    status = models.CharField(
        _("Status"),
        max_length=16,
        choices=STATUS_CHOICES
    )

    @property
    def is_in_progress(self):
        return self.status == self.STATUS_CHOICES.in_progress

    @property
    def is_successful(self):
        return self.status == self.STATUS_CHOICES.succesful

    @property
    def is_unsuccessful(self):
        return self.status == self.STATUS_CHOICES.failed

    @property
    def code(self):
        return self.code_name or self.build_number

    def get_absolute_url(self):
        return u"%s&b=%s" % (self.release.get_absolute_url(), self.build_number)

    def get_ajax_url(self):
        return reverse('build_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return u"{release}.{code}".format(
            release=self.release,
            code=self.code
        )

    class Meta:
        app_label = 'relman'
        ordering = 'build_number',
        unique_together = ('release', 'build_number'),
