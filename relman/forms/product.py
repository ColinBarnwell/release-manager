from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, HTML

from ..models import ProductRelease


class ProductReleaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductReleaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                _("Version"),
                Field('major_version', css_class='input-sm'),
                HTML('.'),
                Field('minor_version', css_class='input-sm'),
                HTML('.'),
                Field('patch_version', css_class='input-sm'),
                HTML('<br />'),
                css_class='form-inline'
            ),
            Fieldset(
                _("Release"),
                Field('target_date'),
                Field('release_manager')
            )
        )

    class Meta:
        model = ProductRelease
        fields = ('release_manager', 'major_version', 'minor_version', 'patch_version', 'target_date')
