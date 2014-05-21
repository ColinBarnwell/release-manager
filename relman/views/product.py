from django.contrib import messages
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, DeleteView, CreateView, UpdateView

from ..forms import (
    ProductForm,
    ProductReleaseCreateForm,
    ProductReleaseEditForm,
    ProductReleaseDependencyCreateForm,
    ReleaseBuildForm,
    CheckCreateForm,
    CheckUpdateForm
)
from ..models import Product, ProductRelease, Build, Check


class ProductCreateView(CreateView):
    model = Product
    template_name = 'relman/includes/modals/create.html'
    form_class = ProductForm


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context_data = super(ProductDetailView, self).get_context_data(**kwargs)
        release = None
        build = None
        if 'v' in self.request.GET:
            try:
                major, minor, patch = self.request.GET['v'].split('.')
                release = ProductRelease.objects.get(
                    product=self.object,
                    major_version=major,
                    minor_version=minor,
                    patch_version=patch
                )
                context_data['release'] = release
            except ValueError, ProductRelease.DoesNotExist:
                pass
        if release is not None and 'b' in self.request.GET:
            try:
                build = release.builds.get(
                    build_number=self.request.GET['b'],
                )
                context_data['build'] = build
            except Build.DoesNotExist:
                pass
        return context_data


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'relman/includes/modals/update.html'
    form_class = ProductForm
    success_url = '/'


class ReleaseCreateView(CreateView):
    model = ProductRelease
    template_name = 'relman/includes/modals/create.html'
    form_class = ProductReleaseCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_pk'])
        return super(ReleaseCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.product
        response = super(ReleaseCreateView, self).form_valid(form)
        previous_versions = self.object.previous_versions()
        if previous_versions:
            self.object.dependencies.add(*previous_versions[0].dependencies.all())
        return response


class ReleaseUpdateView(UpdateView):
    model = ProductRelease
    template_name = 'relman/includes/modals/update.html'
    form_class = ProductReleaseEditForm


class ReleaseDetailView(DetailView):
    model = ProductRelease
    context_object_name = 'release'
    template_name = 'relman/includes/product__release.html'


class ReleaseDeleteView(DeleteView):
    model = ProductRelease
    template_name = 'relman/includes/modals/delete.html'

    def get_success_url(self):
        messages.warning(self.request, _("{object} has been deleted").format(object=self.object))
        return self.object.product.get_absolute_url()


class ReleaseCreateDependencyView(CreateView):
    model = ProductRelease.dependencies.through
    template_name = 'relman/includes/modals/create.html'
    form_class = ProductReleaseDependencyCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.release = get_object_or_404(ProductRelease, pk=kwargs['release_pk'])
        return super(ReleaseCreateDependencyView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(ReleaseCreateDependencyView, self).get_form_kwargs(**kwargs)
        form_kwargs['release'] = self.release
        return form_kwargs

    def form_valid(self, form):
        form.instance.productrelease = self.release
        return super(ReleaseCreateDependencyView, self).form_valid(form)

    def get_success_url(self):
        return self.object.productrelease.get_absolute_url()


class ReleaseDeleteDependencyView(DeleteView):
    model = ProductRelease.dependencies.through
    template_name = 'relman/includes/modals/delete.html'

    def get_object(self):
        return get_object_or_404(
            self.model,
            productrelease_id=self.kwargs['release_pk'],
            packageversion_id=self.kwargs['version_pk']
        )

    def get_context_data(self, **kwargs):
        data = super(ReleaseDeleteDependencyView, self).get_context_data(**kwargs)
        data['delete_message'] = _(
            "Remove {version} as a dependency of {release}?"
        ).format(
            version=self.object.packageversion,
            release=self.object.productrelease
        )
        return data

    def get_success_url(self):
        return self.object.productrelease.get_absolute_url()


class ReleaseBuildDetailView(DetailView):
    model = Build
    context_object_name = 'build'
    template_name = 'relman/includes/product__release__build.html'


class ReleaseBuildCreateView(CreateView):
    model = Build
    template_name = 'relman/includes/modals/create.html'
    form_class = ReleaseBuildForm

    def dispatch(self, request, *args, **kwargs):
        self.release = get_object_or_404(ProductRelease, pk=kwargs['release_pk'])
        return super(ReleaseBuildCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.release = self.release
        current_build_number = self.release.builds.aggregate(
            Max('build_number')
        )['build_number__max']
        if current_build_number is None:
            form.instance.build_number = 1
        else:
            form.instance.build_number = 1 + current_build_number
        return super(ReleaseBuildCreateView, self).form_valid(form)


class ReleaseBuildUpdateView(UpdateView):
    model = Build
    template_name = 'relman/includes/modals/update.html'
    form_class = ReleaseBuildForm

    def get_success_url(self):
        messages.success(self.request, _("{object} has been updated").format(object=self.object))
        return super(ReleaseBuildUpdateView, self).get_success_url()


class CheckCreateView(CreateView):
    model = Check
    template_name = 'relman/includes/modals/create.html'
    form_class = CheckCreateForm

    def dispatch(self, request, *args, **kwargs):
        self.build = get_object_or_404(Build, pk=kwargs['build_pk'])
        return super(CheckCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CheckCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs['build'] = self.build
        return form_kwargs

    def form_valid(self, form):
        form.instance.build = self.build
        return super(CheckCreateView, self).form_valid(form)


class CheckUpdateView(UpdateView):
    model = Check
    template_name = 'relman/includes/modals/update.html'
    form_class = CheckUpdateForm
