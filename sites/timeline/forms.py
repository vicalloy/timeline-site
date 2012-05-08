# -*- coding: UTF-8 -*-
from django import forms

from bootstrap.forms import BootstrapModelForm

#from easy_thumbnails.widgets import ImageClearableFileInput

from .models import Timeline, TlEvent

class TimelineForm(BootstrapModelForm):

    class Meta:
        model = Timeline
        fields = ['title', 'cover', 'tags', 'intro']
        #widgets = { 'cover': ImageClearableFileInput(), }
        
class TlEventForm(BootstrapModelForm):

    class Meta:
        model = TlEvent
        exclude = ['timeline']
        #widgets = { 'cover': ImageClearableFileInput(), }
        
