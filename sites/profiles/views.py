from userena.views import profile_detail as __profile_detail

from timeline.models import get_all_timlines

def profile_detail(request, username):
    ctx = {}
    if request.user.username == username:
        ctx['timelines'] = request.user.timeline_set.exclude(status='del').order_by('-updated_on')
    else:
        ctx['timelines'] = get_all_timlines().filter(created_by=request.user)
    return __profile_detail(request, username, extra_context=ctx)
