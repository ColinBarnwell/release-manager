from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div

from ..models import ProductRelease


class ProductReleaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductReleaseForm, self).__init__(*args, **kwargs)


    class Meta:
        model = ProductRelease
        fields = ('release_manager', 'major_version', 'minor_version', 'patch_version', 'target_date')
