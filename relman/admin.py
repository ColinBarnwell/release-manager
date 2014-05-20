from django.contrib import admin
from django.contrib.contenttypes import generic

from models import (
    Product,
    ProductRelease,
    Build,
    Package,
    PackageVersion,
    PackageVersionBuild,
    Change,
    Checkpoint,
    Check
)


class PackageVersionBuildInline(admin.TabularInline):
    model = PackageVersionBuild
    extra = 1


class PackageVersionInline(admin.StackedInline):
    model = PackageVersion
    extra = 1


class ChangeInline(admin.StackedInline):
    model = Change


class PackageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'current_version', 'next_version')
    inlines = PackageVersionInline,


class PackageVersionAdmin(admin.ModelAdmin):
    inlines = (ChangeInline, PackageVersionBuildInline)


class CheckpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = 'display_order',


admin.site.register(Package, PackageAdmin)
admin.site.register(PackageVersion, PackageVersionAdmin)
admin.site.register(Checkpoint, CheckpointAdmin)
