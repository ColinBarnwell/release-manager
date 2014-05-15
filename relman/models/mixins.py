from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy as _p

from model_utils import Choices


class SoftwareVersion(models.Model):

    STATUS_CHOCIES = Choices(
        ('proposed', _("Proposed")),
        ('in_progress', _("In progress")),
        ('cancelled', _("Cancelled")),
        ('released', _("Released")),
    )

    status = models.CharField(
        _("Status"),
        max_length=16,
        choices=STATUS_CHOCIES
    )

    major_version = models.PositiveIntegerField(_("Major version"), default=0)
    minor_version = models.PositiveIntegerField(_("Minor version"), default=0)
    patch_version = models.PositiveIntegerField(_("Patch version"), default=0)
    alpha_version = models.CharField(_("Alpha version"), max_length=32, blank=True)

    target_date = models.DateField()

    notes = models.TextField(_("Notes"), blank=True)

    def version_number(self):
        return u"{major}.{minor}.{patch}{alpha_sep}{alpha}".format(
            major=self.major_version,
            minor=self.minor_version,
            patch=self.patch_version,
            alpha_sep='.' if self.alpha_version else '',
            alpha=self.alpha_version
        )

    def __unicode__(self, name=''):
        return u"{name}{name_sep}{version_number}".format(
            name=name,
            name_sep=': ' if name else '',
            version_number=self.version_number()
        )

    class Meta:
        abstract = True
        ordering = ('-major_version', '-minor_version', '-patch_version', 'alpha_version')
