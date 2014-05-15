from django.views.generic import DetailView

from ..models import Package


class PackageDetailView(DetailView):
    model = Package
    context_object_name = 'package'
