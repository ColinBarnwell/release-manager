from django.db import models
from django.utils.translation import uggettext_lazy as _, pgettext_lazy as _p

from model_utils import Choices


class Project(models.Model):
    """
    A project is a thing that gets released. It may be a simple application
    with no dependencies, or it might be a complex piece of software pulling
    together multiple packages, each with their own version releases.
    """
    name = models.CharField(
        _p("project name", "Name"),
        max_length=255,
        unique=True
    )


class Release(models.Model):
    """
    A release is an event, either in the past or in the future, that represents
    a project being deployed in a specific state (build version).
    """
    RELEASE_STATUS_CHOCIES = Choices(
        ('cancelled', _("Cancelled")),
        ('in_progress', _("In progress")),
        ('deployed', _("Deployed")),
    )

    project = models.ForeignKey(
        Project,
        verbose_name=(_("Project")),
        editable=False
    )

    release_status = models.CharField(
        _("Build status"),
        max_length=16,
        choices=RELEASE_STATUS_CHOCIES
    )

    notes = models.TextField(_("Notes"), blank=True)

    major_version = models.PositiveIntegerField(default=0)
    minor_version = models.PositiveIntegerField(default=0)
    patch_version = models.PositiveIntegerField(default=0)

    target_date = models.DateField()

    previous_release = models.ForeignKey(
        'Release',
        verbose_name=(_("Previous release")),
        null=True,
        blank=True
    )


class Build(models.Model):
    """
    A build represents a deployment of a release version. A successful build
    is a successful release. An unsuccessful build should be superceded by a
    new build, once code or environment changes have been made.
    """
    BUILD_STATUS_CHOCIES = Choices(
        ('failed', _("Failed")),
        ('in_progress', _("In progress")),
        ('successful', _("Successful")),
    )

    release = models.ForeignKey(
        Release,
        verbose_name=(_("Release")),
        editable=False
    )

    build_number = models.PositiveIntegerField(default=1)

    build_status = models.CharField(
        _("Build status"),
        max_length=16,
        choices=BUILD_STATUS_CHOCIES
    )
