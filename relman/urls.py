from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from views import (
    IndexView,
    ProductCreateView,
    ProductDetailView,
    ProductUpdateView,
    ReleaseCreateView,
    ReleaseDetailView,
    ReleaseUpdateView,
    ReleaseDeleteView,
    ReleaseCreateDependencyView,
    ReleaseDeleteDependencyView,
    BuildCreateView,
    BuildDetailView,
    BuildUpdateView,
    CheckCreateView,
    CheckUpdateView,
    PackageCreateView,
    PackageDetailView,
    PackageUpdateView,
    VersionDetailView,
    CommentsView
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

    url(r'^add_product$', ProductCreateView.as_view(), name='product_create'),
    url(r'^product/(?P<pk>[-\d]+)$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^product/(?P<pk>[-\d]+)/update$', ProductUpdateView.as_view(), name='product_update'),
    url(r'^product/(?P<product_pk>[-\d]+)/add_release$', ReleaseCreateView.as_view(), name='release_create'),

    url(r'^release/(?P<pk>[-\d]+)$', ReleaseDetailView.as_view(), name='release_detail'),
    url(r'^release/(?P<pk>[-\d]+)/update$', ReleaseUpdateView.as_view(), name='release_update'),
    url(r'^release/(?P<pk>[-\d]+)/delete$', ReleaseDeleteView.as_view(), name='release_delete'),
    url(r'^release/(?P<release_pk>[-\d]+)/dependency/create$', ReleaseCreateDependencyView.as_view(), name='release_dependency_create'),
    url(r'^release/(?P<release_pk>[-\d]+)/dependency/(?P<version_pk>[-\d]+)/delete$', ReleaseDeleteDependencyView.as_view(), name='release_dependency_delete'),
    url(r'^release/(?P<release_pk>[-\d]+)/add_build$', BuildCreateView.as_view(), name='build_create'),

    url(r'^build/(?P<pk>[-\d]+)$', BuildDetailView.as_view(), name='build_detail'),
    url(r'^build/(?P<pk>[-\d]+)/update$', BuildUpdateView.as_view(), name='build_update'),
    url(r'^build/(?P<build_pk>[-\d]+)/add_check$', CheckCreateView.as_view(), name='check_create'),

    url(r'^check/(?P<pk>[-\d]+)/update$', CheckUpdateView.as_view(), name='check_update'),

    url(r'^add_package$', PackageCreateView.as_view(), name='package_create'),
    url(r'^package/(?P<pk>[-\d]+)$', PackageDetailView.as_view(), name='package_detail'),
    url(r'^package/(?P<pk>[-\d]+)/update$', PackageUpdateView.as_view(), name='package_update'),
    url(r'^version/(?P<pk>[-\d]+)$', VersionDetailView.as_view(), name='version_detail'),
    url(r'^comments/(?P<content_type>[-\d]+)/(?P<object_id>[-\d]+)$', CommentsView.as_view(), name='comments_list')
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^403.html$', TemplateView.as_view(template_name='403.html')),
        url(r'^404.html$', TemplateView.as_view(template_name='404.html')),
        url(r'^500.html$', TemplateView.as_view(template_name='500.html')),
    ]
