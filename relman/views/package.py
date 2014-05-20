from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from ..forms import PackageForm, PackageVersionCreateForm, PackageVersionEditForm
from ..models import Package, PackageVersion


class PackageCreateView(CreateView):
    model = Package
    template_name = 'relman/includes/modals/create.html'
    form_class = PackageForm

    def get_success_url(self):
        messages.success(self.request, _("{object} has been created").format(object=self.object))
        return super(PackageCreateView, self).get_success_url()


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


class PackageUpdateView(UpdateView):
    model = Package
    template_name = 'relman/includes/modals/update.html'
    form_class = PackageForm

    def get_success_url(self):
        messages.success(self.request, _("{object} has been updated").format(object=self.object))
        return '/'


class VersionCreateView(CreateView):
    model = PackageVersion
    template_name = 'relman/includes/modals/create.html'
    form_class = PackageVersionCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.package = get_object_or_404(Package, pk=kwargs['package_pk'])
        return super(VersionCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.package = self.package
        return super(VersionCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("{object} has been created").format(object=self.object))
        return super(VersionCreateView, self).get_success_url()


class VersionUpdateView(UpdateView):
    model = PackageVersion
    template_name = 'relman/includes/modals/update.html'
    form_class = PackageVersionEditForm

    def get_success_url(self):
        messages.success(self.request, _("{object} has been updated").format(object=self.object))
        return super(VersionUpdateView, self).get_success_url()


class VersionDeleteView(DeleteView):
    model = PackageVersion
    template_name = 'relman/includes/modals/delete.html'

    def get_success_url(self):
        messages.warning(self.request, _("{object} has been deleted").format(object=self.object))
        return self.object.package.get_absolute_url()


class VersionDetailView(DetailView):
    model = PackageVersion
    context_object_name = 'version'
    template_name = 'relman/includes/package__version.html'
