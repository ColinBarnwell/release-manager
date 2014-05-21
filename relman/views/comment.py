from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, CreateView

from ..forms import CommentForm
from ..models import Comment

from mixins import RequireAuthenticatedUser


class CommentsView(RequireAuthenticatedUser, ListView, CreateView):

    model = Comment
    template_name = 'relman/includes/modals/comments.html'
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        ct = get_object_or_404(
            ContentType,
            pk=self.kwargs['content_type']
        )
        self.content_object = get_object_or_404(
            ct.model_class(),
            pk=self.kwargs['object_id']
        )
        return super(CommentsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(CommentsView, self).get_context_data(**kwargs)
        data['form'] = self.form_class()
        return data

    def get_queryset(self):
        self.object = None
        return Comment.objects.filter(
            content_type=self.kwargs['content_type'],
            object_id=self.kwargs['object_id']
        )

    def get_success_url(self):
        messages.success(self.request, _("Your comment has been added"))
        return self.content_object.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.content_type_id = self.kwargs['content_type']
        form.instance.object_id = self.kwargs['object_id']
        return super(CommentsView, self).form_valid(form)
