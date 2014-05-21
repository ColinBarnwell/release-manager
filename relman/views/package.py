from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from ..forms import PackageForm, PackageVersionCreateForm, PackageVersionEditForm, VersionBuildForm, VersionChangeForm
from ..models import Package, PackageVersion, PackageVersionBuild, Change


class PackageCreateView(CreateView):
    model = Package
    template_name = 'relman/includes/modals/create.html'
    form_class = PackageForm


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
    success_url = '/'


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


class VersionUpdateView(UpdateView):
    model = PackageVersion
    template_name = 'relman/includes/modals/update.html'
    form_class = PackageVersionEditForm


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


class VersionBuildCreateView(CreateView):
    model = PackageVersionBuild
    template_name = 'relman/includes/modals/create.html'
    form_class = VersionBuildForm

    def dispatch(self, request, *args, **kwargs):
        self.version = get_object_or_404(PackageVersion, pk=kwargs['version_pk'])
        return super(VersionBuildCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(VersionBuildCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs['version'] = self.version
        return form_kwargs

    def form_valid(self, form):
        form.instance.version = self.version
        return super(VersionBuildCreateView, self).form_valid(form)


class VersionBuildUpdateView(UpdateView):
    model = PackageVersionBuild
    template_name = 'relman/includes/modals/update.html'
    form_class = VersionBuildForm


class VersionChangeCreateView(CreateView):
    model = Change
    template_name = 'relman/includes/modals/create.html'
    form_class = VersionChangeForm

    def dispatch(self, request, *args, **kwargs):
        self.version = get_object_or_404(PackageVersion, pk=kwargs['version_pk'])
        return super(VersionChangeCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(VersionChangeCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs['version'] = self.version
        return form_kwargs

    def form_valid(self, form):
        form.instance.version = self.version
        return super(VersionChangeCreateView, self).form_valid(form)


class VersionChangeUpdateView(UpdateView):
    model = Change
    template_name = 'relman/includes/modals/update.html'
    form_class = VersionChangeForm


class VersionChangeDeleteView(DeleteView):
    model = Change
    template_name = 'relman/includes/modals/delete.html'

    def get_success_url(self):
        messages.warning(self.request, _("Change has been deleted"))
        return self.object.get_absolute_url()
