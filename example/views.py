from django.shortcuts import render, get_object_or_404

from laboratory.models import Study

def home(request):    

	studies = Study.objects.all()
	return render(request, 'home.html', locals())