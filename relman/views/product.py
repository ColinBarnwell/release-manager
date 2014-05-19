from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, DeleteView

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
                pass
        return context_data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


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
