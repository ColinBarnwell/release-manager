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


class ProductReleaseDependencyCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.release = kwargs.pop('release', None)
        super(ProductReleaseDependencyCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.fields['packageversion'].label = _("Package version")

    def clean_packageversion(self):
        if ProductRelease.dependencies.through.objects.filter(
            productrelease=self.release,
            packageversion=self.cleaned_data['packageversion']
        ).exists():
            raise forms.ValidationError(
                _("This dependency already exists")
            )
        if ProductRelease.dependencies.through.objects.filter(
            productrelease=self.release,
            packageversion__package=self.cleaned_data['packageversion'].package
        ).exists():
            raise forms.ValidationError(
                _("A dependency already exists for this package")
            )
        return self.cleaned_data['packageversion']

    class Meta:
        model = ProductRelease.dependencies.through
        fields = (
            'packageversion',
        )


class ReleaseBuildForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReleaseBuildForm, self).__init__(*args, **kwargs)
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
