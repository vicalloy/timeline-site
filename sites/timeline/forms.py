# -*- coding: UTF-8 -*-
from bootstrap.forms import BootstrapModelForm

#from easy_thumbnails.widgets import ImageClearableFileInput

from .models import Timeline, TlEvent

class TimelineForm(BootstrapModelForm):

    class Meta:
        model = Timeline
        fields = ['title', 'cover', 'tags', 'intro']
        #widgets = { 'cover': ImageClearableFileInput(), }
        
class TlEventForm(BootstrapModelForm):

    def clean_startdate(self):
        v = self.cleaned_data['startdate']
        #TODO valid_date
        return v

    def clean_enddate(self):
        v = self.cleaned_data['enddate']
        #TODO valid_date
        return v

    def save(self, *args, **kwargs):
        tlevent = super(TlEventForm, self).save(*args, **kwargs)
        if tlevent.cover:
            for e in TlEvent.objects.filter(cover=True).exclude(pk=tlevent.pk):
                e.cover = False
                e.save()
        return tlevent

    class Meta:
        model = TlEvent
        exclude = ['timeline']
        #widgets = { 'cover': ImageClearableFileInput(), }

