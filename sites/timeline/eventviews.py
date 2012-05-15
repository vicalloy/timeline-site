from django.shortcuts import render, get_object_or_404, redirect

from ajax_validation.utils import render_json_response

from models import TlEvent

#TODO load new events form
#TODO load edit events form
def delete_(request):
    #TODO auth
    pk = request.GET.get('pk', '')
    tl = get_object_or_404(TlEvent, pk=pk)
    tl.delete()
    #TODO message
    return render_json_response({'valid': True})
