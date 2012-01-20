# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Timeline, Recommend

admin.site.register(Timeline)
admin.site.register(Recommend)
