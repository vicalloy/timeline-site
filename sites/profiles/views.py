from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from userena.views import profile_detail as __profile_detail

from timeline.models import get_all_timlines

def profile_detail(request, username):
    ctx = {}
    view_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated() and request.user.username == username:
        ctx['timelines'] = view_user.timeline_set.exclude(status='del').order_by('-updated_on')
    else:
        ctx['timelines'] = get_all_timlines().filter(created_by=view_user)
    return __profile_detail(request, username, extra_context=ctx)
