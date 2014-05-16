from django.contrib import admin

from models import (
    Product,
    ProductRelease,
    Build,
    Package,
    PackageVersion,
    Change,
    Environment,
    Promotion
)


class BuildInline(admin.TabularInline):
    model = Build
    extra = 1


class PromotionInline(admin.TabularInline):
    model = Promotion
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


class BuildAdmin(admin.ModelAdmin):
    inlines = PromotionInline,


class PackageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'current_version', 'next_version')
    inlines = PackageVersionInline,


class PackageVersionAdmin(admin.ModelAdmin):
    inlines = ChangeInline,


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductRelease, ProductReleaseAdmin)
admin.site.register(Build, BuildAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(PackageVersion, PackageVersionAdmin)
admin.site.register(Environment)
