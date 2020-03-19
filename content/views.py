from django.shortcuts import render
from .models import Content
from django.http import HttpResponse, HttpResponseBadRequest, Http404, JsonResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist

# Return content titles
def get_content(request):
	
	if request.method == 'GET':
		contents = Content.objects.all()
		return JsonResponse( { content.title : '/content/{}/'.format(str(content.pk)) for content in contents } )
	
	return HttpResponseBadRequest("Must be a GET Request to access this resource")

def content_view(request, content_pk=-1):
	content = None
	
	if request.method != 'GET':
		return HttpResponseBadRequest("Must be a GET Request to access this reource")

	try:
		content = Content.objects.all().get(pk = content_pk)
	except ObjectDoesNotExist as e:
		raise Http404

	return render(request, "content/content.html", context = {'content':content})

