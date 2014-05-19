from django.views.generic import ListView

from ..models import Comment


class CommentsView(ListView):

    template_name = 'relman/includes/modals/comments.html'

    def get_queryset(self):
        return Comment.objects.filter(
            content_type=self.kwargs['content_type'],
            object_id=self.kwargs['object_id']
        )
