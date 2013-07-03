from django.contrib import admin
from django.forms import Form, ModelForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.conf.urls import patterns, include, url

from models import Study, Group, LabPage

### Custom Admins ###
class StudyAdmin(admin.ModelAdmin):
    pass

class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['participants',]    

admin.site.register(Group, GroupAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(LabPage)