import re

from django.template import Library
from django.utils.safestring import mark_safe

from timeline.models import get_all_timlines
from timeline.helper import _html, tl_markdown

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

@register.filter
def md(_md):
    return tl_markdown(_md)

@register.filter
def media2html(media):
    def _is_link(media):
        return re.search('^(http|HTTP)://\S*$', 
                media)
    def _is_img(media):
        return re.search('^(http|HTTP)://\S*(?i)\\.(jpg|bmp|png|gif|img|jng|jpeg|jpe|gif|giff)$', 
                media)
    if _is_img(media):
        html = u'<img src="%s"/>' % _html(media)
        return mark_safe(html)
    if _is_link(media):
        html = u'<a target="_blank" href="%s">%s</a>' % (_html(media), _html(media))
        return mark_safe(html)
    return media
