import os

from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext, Context, Template

from laboratory.models import Study, LabPage
from laboratory.forms import ParticipantsForm


def page(request, page):
	lab_page = LabPage.objects.get(slug=page)
	return render(request, 'laboratory/lab_page.html', locals())

@staff_member_required
def study(request, study):
    study = Study.objects.get(pk=study)        
    form = ParticipantsForm(request, study=study)
    if form.is_valid():
        form.save()    
    return render(request, 'laboratory/study_editor.html', locals())
    

