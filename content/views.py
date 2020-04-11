from django.shortcuts import render
from .models import Content
from django.http import HttpResponse, HttpResponseBadRequest, Http404, JsonResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

"""
Return content titles in a json with this form:
{ 
	Content_Title : content_url,
}
"""
def get_content(request):
	
	if request.method == 'GET':
		contents = Content.objects.all()
		return JsonResponse( { content.title : '/content/{}/'.format(str(content.pk)) for content in contents if content.title not in settings.CONTENT_KEY_NAMES.values() } )
	
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

def landing_page(request):
	lp = None
	try: 
		lp = Content.objects.all().get(title = settings.CONTENT_KEY_NAMES.get('LANDING_PAGE_CONTENT_NAME', None))
	except Content.DoesNotExist:
		print("Landing page object does not exist")
	return render(request, "landing_page.html", context = {"content":lp})