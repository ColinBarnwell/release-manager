from django.conf.urls import include, url
from django.contrib import admin

import views


admin.autodiscover()

urlpatterns = [

    #Login
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', {'login_url': '/'}),

    # Admin
    url(r'^djadmn/doc/', include('django.contrib.admindocs.urls')),
    url(r'^djadmn/', include(admin.site.urls)),

    # Index
    url(r'^$', views.IndexView.as_view(), name='index'),

    # Products
    url(r'^add_product$', views.ProductCreateView.as_view(), name='product_create'),
    url(r'^product/(?P<pk>[-\d]+)$', views.ProductDetailView.as_view(), name='product_detail'),
    url(r'^product/(?P<pk>[-\d]+)/update$', views.ProductUpdateView.as_view(), name='product_update'),

    # Product releases
    url(r'^product/(?P<product_pk>[-\d]+)/add_release$', views.ReleaseCreateView.as_view(), name='release_create'),
    url(r'^release/(?P<pk>[-\d]+)$', views.ReleaseDetailView.as_view(), name='release_detail'),
    url(r'^release/(?P<pk>[-\d]+)/update$', views.ReleaseUpdateView.as_view(), name='release_update'),
    url(r'^release/(?P<pk>[-\d]+)/delete$', views.ReleaseDeleteView.as_view(), name='release_delete'),
    url(r'^release/(?P<release_pk>[-\d]+)/dependency/create$', views.ReleaseCreateDependencyView.as_view(), name='release_dependency_create'),
    url(r'^release/(?P<release_pk>[-\d]+)/dependency/(?P<version_pk>[-\d]+)/delete$', views.ReleaseDeleteDependencyView.as_view(), name='release_dependency_delete'),
    url(r'^release/(?P<release_pk>[-\d]+)/add_build$', views.ReleaseBuildCreateView.as_view(), name='build_create'),

    # Release builds
    url(r'^build/(?P<pk>[-\d]+)$', views.ReleaseBuildDetailView.as_view(), name='build_detail'),
    url(r'^build/(?P<pk>[-\d]+)/update$', views.ReleaseBuildUpdateView.as_view(), name='build_update'),
    url(r'^build/(?P<build_pk>[-\d]+)/add_check$', views.CheckCreateView.as_view(), name='check_create'),
    url(r'^check/(?P<pk>[-\d]+)/update$', views.CheckUpdateView.as_view(), name='check_update'),

    # Packages
    url(r'^add_package$', views.PackageCreateView.as_view(), name='package_create'),
    url(r'^package/(?P<pk>[-\d]+)$', views.PackageDetailView.as_view(), name='package_detail'),
    url(r'^package/(?P<pk>[-\d]+)/update$', views.PackageUpdateView.as_view(), name='package_update'),

    # Package versions
    url(r'^package/(?P<package_pk>[-\d]+)/add_version$', views.VersionCreateView.as_view(), name='version_create'),
    url(r'^version/(?P<pk>[-\d]+)$', views.VersionDetailView.as_view(), name='version_detail'),
    url(r'^version/(?P<pk>[-\d]+)/update$', views.VersionUpdateView.as_view(), name='version_update'),
    url(r'^version/(?P<pk>[-\d]+)/delete$', views.VersionDeleteView.as_view(), name='version_delete'),

    # Version builds
    url(r'^version/(?P<version_pk>[-\d]+)/add_build$', views.VersionBuildCreateView.as_view(), name='versionbuild_create'),
    url(r'^version-build/(?P<pk>[-\d]+)/update$', views.VersionBuildUpdateView.as_view(), name='versionbuild_update'),

    # Version changes
    url(r'^version/(?P<version_pk>[-\d]+)/add_change$', views.VersionChangeCreateView.as_view(), name='change_create'),
    url(r'^change/(?P<pk>[-\d]+)/update$', views.VersionChangeUpdateView.as_view(), name='change_update'),
    url(r'^change/(?P<pk>[-\d]+)/delete$', views.VersionChangeDeleteView.as_view(), name='change_delete'),

    # Comments
    url(r'^comments/(?P<content_type>[-\d]+)/(?P<object_id>[-\d]+)$', views.CommentsView.as_view(), name='comments_list')

]
