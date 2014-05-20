from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, DeleteView, CreateView, UpdateView

from ..forms import ProductReleaseForm
from ..models import Product, ProductRelease, Build


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context_data = super(ProductDetailView, self).get_context_data(**kwargs)
        context_data['new_release_form'] = ProductReleaseForm(self.request.POST or None)
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
                release = None
        if 'b' in self.request.GET:
            try:
                build = Build.objects.get(
                    pk=self.request.GET['b'],
                    release=release,
                )
                context_data['build'] = build
            except Build.DoesNotExist:
                build = None
        return context_data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ReleaseCreateView(CreateView):
    model = ProductRelease
    template_name = 'relman/includes/modals/create.html'
    form_class = ProductReleaseForm

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs['product_pk'])
        return super(ReleaseCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.product
        return super(ReleaseCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("{object} has been created").format(object=self.object))
        return super(ReleaseCreateView, self).get_success_url()


class ReleaseUpdateView(UpdateView):
    model = ProductRelease
    template_name = 'relman/includes/modals/update.html'
    form_class = ProductReleaseForm

    def get_success_url(self):
        messages.success(self.request, _("{object} has been updated").format(object=self.object))
        return super(ReleaseUpdateView, self).get_success_url()


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


class BuildDetailView(DetailView):
    model = Build
    context_object_name = 'build'
    template_name = 'relman/includes/product__release__build.html'
