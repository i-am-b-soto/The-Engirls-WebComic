from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from django.db.models import F
from .filters import ComicPanelFilter
from .models import ComicPanel#, Comment
from comments.forms import CommentForm
from social_django.models import UserSocialAuth
from django.db.utils import OperationalError
from dal import autocomplete


# View for most recent comic
def index(request):
	if request.method == 'GET':

		# Let's find the most recent comic!
		comic_to_display= None

		# Make sure there is a series labeled 'main'
		if ComicPanel.objects.filter(series=settings.MAIN_SERIES_NAME).exists():
		
			# Get the chapters for the main series
			chapter_dicts = ComicPanel.objects.filter(series=settings.MAIN_SERIES_NAME).values('chapter').distinct()
			chapters = []
			for item in chapter_dicts:
				if item['chapter']:
					chapters.append(item['chapter'])

			if chapters:
				finalChapter = max(chapters)
				comic_to_display = ComicPanel.objects.filter(
					series=settings.MAIN_SERIES_NAME,
					chapter=finalChapter
					).order_by(F("page").desc(nulls_last = True)).first()
			
			# If there are not chapters...
			else:
				comic_to_display = ComicPanel.objects.all().order_by("-uploadTime").first()

		else:
			comic_to_display = ComicPanel.objects.all().order_by("-uploadTime").first()

		# Null Check
		if comic_to_display:
			return view_panel(request, comic_to_display.pk)
		else: 
			return view_panel(request)


"""
Return dictionary of chapters per series
I.E. 

{
	"1.0": {
		"id":1.0,
		"name": 1.0
	},
	"2.0":{ ... }
}
"""
def auto_complete_chapter(request):
	series = request.GET.get('series', None)
	data = {}

	if series:
		chapters_list = []	
		if series:
			chapters_dicts = ComicPanel.objects.filter(series = series).values_list('chapter').distinct()
			chapters_list = [(item[0],item[0]) for item in chapters_dicts]
			data = { chapter[0]: {'id': chapter[0], 'name': chapter[1] } for chapter in chapters_list}	

	return JsonResponse(data)

def auto_complete_page(request):
	series = request.GET.get('series', None)
	chapter = request.GET.get('chapter', None)
	data = {}

	if series and chapter:
		pages_dicts = ComicPanel.objects.filter(series = series, chapter = chapter).values_list('page').distinct()
		page_list = [(item[0], item[0]) for item in pages_dicts]
		data = {page[0]: {'id':page[0], 'name':page[1]} for page in page_list}

	return JsonResponse(data)
		


# View Archive
def view_archive(request):

	comic_list = ComicPanel.objects.order_by('series', 'chapter', 'page')
	filter_list = {}

	if request.GET.get('series', None):
		filter_list['series__exact'] = request.GET.get('series')

	if request.GET.get('chapter', None) and request.GET.get('chapter') is not 'null':
		filter_list['chapter__exact'] = request.GET.get('chapter')

	if request.GET.get('page', None) and request.GET.get('page') is not 'null':
		filter_list['page__exact'] = request.GET.get('page')

	comic_list = comic_list.filter(**filter_list)

	comic_filter = ComicPanelFilter(request.GET, queryset=comic_list)
	paginator = Paginator(comic_filter.qs, settings.COMIC_PAGINATOR_COUNT)

	page = request.GET.get('web_page', 1)
	try:
		comics = paginator.page(page)
	except (PageNotAnInteger, TypeError):
		comics = paginator.page(1)
	except EmptyPage:
		comics = paginator.page(paginator.num_pages)

	return render(request, 'comics/comic_archive.html', context = {'filter': comic_filter, 'comics': comics})	

# View for specific comic
def view_panel(request, comic_pk =-1 ):

	comic_panel = None
	newest_comic_pk = -1
	oldest_comic_pk = -1
	next_comic_pk = -1
	prev_comic_pk = -1
	comment_form = CommentForm()

	#print("comic_pk:{}".format(str(comic_pk)))
	# Try to get comment with given pk. Return default values otherwise
	try:
		comic_panel = ComicPanel.objects.all().get(pk=comic_pk)
	except ObjectDoesNotExist:
		raise Http404

	# Get chapters
	chapter_dicts = ComicPanel.objects.filter(series = comic_panel.series).values('chapter').distinct()
	chapters = []
	for item in chapter_dicts:
		if item['chapter']:
			chapters.append(item['chapter'])         

	# If Chapters exists
	if chapters and comic_panel.chapter is not None:

		finalChapter = max(chapters)
		newest_comic_pk = ComicPanel.objects.filter(
			series = comic_panel.series, 
			chapter=finalChapter).order_by(F("page").desc(nulls_last=True)).first().pk


		firstChapter = min(chapters)
		oldest_comic_pk = final_comic = ComicPanel.objects.filter(
			series = comic_panel.series, chapter=firstChapter).order_by(F("page").asc(nulls_last=True)).first().pk

		# Do we have a page? Find the next, previous and first
		if comic_panel.page:

			# Is the next page in the current chaper?
			if ComicPanel.objects.filter(series = comic_panel.series, chapter=comic_panel.chapter, page = comic_panel.page+1).exists():
				next_comic_pk = ComicPanel.objects.all().get(
						series=comic_panel.series, chapter=comic_panel.chapter, page=comic_panel.page + 1).pk 
				
			# Is the next page in another chaper?
			elif comic_panel.chapter +1 in chapters:
				next_comic_pk = ComicPanel.objects.all().get(
					series = comic_panel.series,
					chapter = comic_panel.chapter+1, 
					page = ComicPanel.objects.filter(
						chapter = comic_panel.chapter +1).order_by(F("page").asc(nulls_last=True)).first().page).pk
					
			# Is the previous page in the current chapter?
			if ComicPanel.objects.filter(series = comic_panel.series, chapter=comic_panel.chapter, page = comic_panel.page -1).exists():
				prev_comic_pk = ComicPanel.objects.all().get(
					series = comic_panel.series, 
					chapter=comic_panel.chapter, 
					page = comic_panel.page -1).pk

			# Is the previous page in the previous chapter?
			elif comic_panel.chapter -1 in chapters:

				#Find the last page in the previous chapter  
				prev_comic_pk = ComicPanel.objects.all().get(
					series = comic_panel.series,
					chapter=comic_panel.chapter -1, 
					page=ComicPanel.objects.filter(
						chapter = comic_panel.chapter -1).order_by(F("page").desc(nulls_last=True)).first().page).pk
			
	return render(request, 'comics/comic_panel_view.html',
		context = {'comic_panel': comic_panel,
		'newest_comic_pk': newest_comic_pk,
		'oldest_comic_pk': oldest_comic_pk,
		'prev_comic_pk' : prev_comic_pk,
		'next_comic_pk': next_comic_pk,
		'comment_form':comment_form
									  })
#def view_blog_comments(request, post)


