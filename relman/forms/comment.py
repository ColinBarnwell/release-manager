from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from ..models import Comment


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('notes', rows=5),
        )

    class Meta:
        model = Comment
        fields = ('notes',)
