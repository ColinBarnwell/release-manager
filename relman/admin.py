from django.contrib import admin
from django.contrib.contenttypes import generic

from models import (
    Comment,
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


class CommentGenericInline(generic.GenericStackedInline):
    model = Comment
    extra = 1


class BuildInline(admin.TabularInline):
    model = Build
    extra = 1

class PackageVersionBuildInline(admin.TabularInline):
    model = PackageVersionBuild
    extra = 1


class CheckInline(admin.TabularInline):
    model = Check
    extra = 1


class PackageVersionInline(admin.StackedInline):
    model = PackageVersion
    extra = 1


class ChangeInline(admin.StackedInline):
    model = Change


class ProductAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'current_release', 'next_release')


class ProductReleaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'status', 'target_date')
    inlines = CommentGenericInline,


class BuildAdmin(admin.ModelAdmin):
    inlines = CheckInline,


class PackageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'current_version', 'next_version')
    inlines = PackageVersionInline,


class PackageVersionAdmin(admin.ModelAdmin):
    inlines = (ChangeInline, PackageVersionBuildInline)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductRelease, ProductReleaseAdmin)
admin.site.register(Build, BuildAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(PackageVersion, PackageVersionAdmin)
admin.site.register(Checkpoint)
