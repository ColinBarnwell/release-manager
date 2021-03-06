from django.views.generic import TemplateView

from ..models import Product, Package

from mixins import RequireAuthenticatedUser


class IndexView(RequireAuthenticatedUser, TemplateView):

    template_name = 'relman/index.html'

    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        data['packages'] = Package.objects.all()
        return data
