from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML

from ..models import Product, ProductRelease, Build, Check


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        model = Product
        fields = ('name',)


class ProductReleaseCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductReleaseCreateForm, self).__init__(*args, **kwargs)
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
                Field('release_manager')
            ),
        )

    class Meta:
        model = ProductRelease
        fields = (
            'release_manager',
            'major_version',
            'minor_version',
            'patch_version',
            'target_date',
        )


class ProductReleaseEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductReleaseEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('target_date'),
            Field('status'),
            Field('release_manager'),
            Field('notes')
        )

    class Meta:
        model = ProductRelease
        fields = (
            'release_manager',
            'target_date',
            'status',
            'notes'
        )


class BuildForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BuildForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        model = Build
        fields = (
            'code_name',
            'status'
        )


class CheckCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.build = kwargs.pop('build', None)
        super(CheckCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    def clean_checkpoint(self):
        if Check.objects.filter(
            build=self.build,
            checkpoint=self.cleaned_data['checkpoint']
        ).exists():
            raise forms.ValidationError(
                _("Checkpoint already exists for this build.")
            )
        return self.cleaned_data['checkpoint']

    class Meta:
        model = Check
        fields = (
            'checkpoint',
            'status',
        )


class CheckUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CheckUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    class Meta:
        model = Check
        fields = (
            'status',
        )
