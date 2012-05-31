from django.template import Library

from timeline.models import get_all_timlines

register = Library()

@register.inclusion_tag('dummy.html')
def tl_hot(template='timeline/widgets/hot.html'):
    return {'template': template,
            'timelines': get_all_timlines().order_by('-num_views')[:5] }

@register.inclusion_tag('dummy.html')
def tl_last(template='timeline/widgets/last.html'):
    return {'template': template,
            'timelines': get_all_timlines().order_by('-updated_on')[:5] }

@register.inclusion_tag('dummy.html')
def tl_recommend(template='timeline/widgets/recommend.html'):
    return {'template': template,
            'timelines': get_all_timlines().order_by('-rec_on')[:5] }
