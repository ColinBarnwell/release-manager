from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML

from ..models import Package, PackageVersion


class PackageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        model = Package
        fields = ('name',)


class PackageVersionCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PackageVersionCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('major_version', css_class='input-sm'),
                HTML('.'),
                Field('minor_version', css_class='input-sm'),
                HTML('.'),
                Field('patch_version', css_class='input-sm'),
                css_class='form-inline'
            ),
            HTML('<hr />'),
            Div(
                _("Release"),
                Field('target_date'),
            ),
        )

    class Meta:
        model = PackageVersion
        fields = (
            'major_version',
            'minor_version',
            'patch_version',
            'target_date',
        )


class PackageVersionEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PackageVersionEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('target_date'),
            Field('status'),
            Field('notes')
        )

    class Meta:
        model = PackageVersion
        fields = (
            'target_date',
            'status',
            'notes'
        )