from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from views import (
    IndexView,
    ProductDetailView,
    ReleaseDetailView,
    BuildDetailView,
    PackageDetailView,
    VersionDetailView
)


admin.autodiscover()

urlpatterns = [

    #Login
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {'login_url': '/'}),

    # Admin
    url(r'^djadmn/doc/', include('django.contrib.admindocs.urls')),
    url(r'^djadmn/', include(admin.site.urls)),

    # Release Manager
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^product/(?P<pk>[-\d]+)$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^release/(?P<pk>[-\d]+)$', ReleaseDetailView.as_view(), name='release_detail'),
    url(r'^build/(?P<pk>[-\d]+)$', BuildDetailView.as_view(), name='build_detail'),
    url(r'^package/(?P<pk>[-\d]+)$', PackageDetailView.as_view(), name='package_detail'),
    url(r'^version/(?P<pk>[-\d]+)$', VersionDetailView.as_view(), name='version_detail')
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^403.html$', TemplateView.as_view(template_name='403.html')),
        url(r'^404.html$', TemplateView.as_view(template_name='404.html')),
        url(r'^500.html$', TemplateView.as_view(template_name='500.html')),
    ]
