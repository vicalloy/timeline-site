from django.shortcuts import get_object_or_404

from ajax_validation.views import validate_form
from ajax_validation.utils import render_json_response

from .forms import TlEventForm
from .models import TlEvent
from .helper import event_to_sdict

def delete_(request):
    pk = request.GET.get('pk', '')
    event = get_object_or_404(TlEvent, pk=pk)
    if not event.timeline.can_edit(request.user):
        return render_json_response({'valid': False})
    event.delete()
    timeline = event.timeline
    timeline.update_num_events()
    timeline.update_updated_on()
    return render_json_response({'valid': True})

def json_(request):
    pk = request.GET.get('pk', '')
    event = TlEvent.objects.get(pk=pk)
    data = {'valid': True}
    data['data'] = event_to_sdict(event)
    return render_json_response(data)

def edit_(request):
    pk = request.GET.get('pk', '')
    event = TlEvent.objects.get(pk=pk)
    if not event.timeline.can_edit(request.user):
        return render_json_response({'valid': False})
    form, validate = validate_form(request, form_class=TlEventForm, instance=event)
    if validate['valid']:
        event = form.save()
        event.timeline.update_updated_on()
        validate['data'] = event_to_sdict(event)
    return render_json_response(validate)
