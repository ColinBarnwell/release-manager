from django.views.generic import DetailView

from ..models import Product, ProductRelease, Build


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        data = super(ProductDetailView, self).get_context_data(**kwargs)
        if 'v' in self.request.GET:
            try:
                major, minor, patch = self.request.GET['v'].split('.')
                release = ProductRelease.objects.get(
                    product=self.object,
                    major_version=major,
                    minor_version=minor,
                    patch_version=patch
                )
                data['release'] = release
            except ValueError, ProductRelease.DoesNotExist:
                pass
        return data


class ReleaseDetailView(DetailView):
    model = ProductRelease
    context_object_name = 'release'
    template_name = 'relman/includes/product__release.html'


class BuildDetailView(DetailView):
    model = Build
    context_object_name = 'build'
    template_name = 'relman/includes/product__release__build.html'
