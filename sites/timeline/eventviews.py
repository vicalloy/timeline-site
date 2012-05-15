from django.shortcuts import render, get_object_or_404, redirect

from ajax_validation.utils import render_json_response

from models import TlEvent
from helper import event_to_sdict

#TODO load new events form
#TODO load edit events form
def delete_(request):
    #TODO auth
    pk = request.GET.get('pk', '')
    tl = get_object_or_404(TlEvent, pk=pk)
    tl.delete()
    #TODO message
    return render_json_response({'valid': True})

def json_(request):
    pk = request.GET.get('pk', '')
    event = TlEvent.objects.get(pk=pk)
    data = {'valid': True};
    data['data'] = event_to_sdict(event)
    return render_json_response(data)

def edit_(request, pk):
    pk = request.GET.get('pk', '')
    event = TlEvent.objects.get(pk=pk)
    form, validate = validate_form(request, form_class=TlEventForm, instance=event)
    if validate['valid']:
        event = form.save(commit=False)
        event.save()
        validate['data'] = event_to_sdict(event)
    return render_json_response(validate)
