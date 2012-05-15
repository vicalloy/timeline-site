# -*- coding: UTF-8 -*-
def _fmt_date(d):
    #return "%02d,%02d,%02d" % (d.year,d.month,d.day) if d else ''
    return d.replace('-', ',') if d else ''

def event_to_dict(e):
    return {'startDate': fmt_date(e.startdate),
            'endDate': fmt_date(e.enddate),
            'headline': e.title,
            'text': e.text,
            'pk': e.pk,
            "asset": {
                "media": e.media,
                "credit": e.media_credit,
                "caption": e.media_caption }
            }

def event_to_sdict(e):
    return {'startdate': e.startdate,
            'enddate': e.enddate,
            'title': e.title,
            'text': e.text,
            'pk': e.pk,
            'media': e.media,
            'media_credit': e.media_credit,
            'media_caption': e.media_caption,
            }
