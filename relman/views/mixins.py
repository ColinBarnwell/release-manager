from django.core.urlresolvers import reverse
from django.shortcuts import redirect


class RequireAuthenticatedUser(object):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect(reverse('login'))
        return super(RequireAuthenticatedUser, self).dispatch(request, *args, **kwargs)
