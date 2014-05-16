from django.views.generic import DetailView

from ..models import Package, PackageVersion


class PackageDetailView(DetailView):
    model = Package
    context_object_name = 'package'

    def get_context_data(self, **kwargs):
        data = super(PackageDetailView, self).get_context_data(**kwargs)
        if 'v' in self.request.GET:
            try:
                major, minor, patch = self.request.GET['v'].split('.')
                version = PackageVersion.objects.get(
                    package=self.object,
                    major_version=major,
                    minor_version=minor,
                    patch_version=patch
                )
                data['version'] = version
            except ValueError, PackageVersion.DoesNotExist:
                pass
        return data


class VersionDetailView(DetailView):
    model = PackageVersion
    context_object_name = 'version'
    template_name = 'relman/includes/package__version.html'
