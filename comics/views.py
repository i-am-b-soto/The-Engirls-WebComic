
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import ComicPanel
from django.http import HttpResponse, Http404
from .forms import ArchiveSearchForm, getSeriesNames
from django.template import loader, RequestContext
from django.conf import settings
from django.db.models import F
#from dal import autocomplete
from .filters import ComicPanelFilter


""" Counter class used for django templates """
class Counter:
	count = 0

	def increment(self):
		self.count = self.count +1
		return ''

	def decrement(self):
		self.count = self.count -1
		return ''


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
					).order_by(F("episode").desc(nulls_last = True)).first()
			
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
class SeriesAutocomplete(autocomplete.Select2ListView):

	def get_list(self):
		return list (ComicPanel.objects.values('series_name').distinct())
"""

def view_archive(request):
	#Attempting to write this method with djando filters
	"""
		For filter references:
			https://django-filter.readthedocs.io/en/stable/guide/usage.html#the-filter
			https://stackoverflow.com/questions/44048156/django-filter-use-paginations
	"""
	comic_list = ComicPanel.objects.all()
	comic_filter = ComicPanelFilter(request.GET, queryset=comic_list)
	paginator = Paginator(comic_filter.qs, 8)
	#TODO: Why 1? 
	page = request.GET.get('page', 1)
	try:
		comics = paginator.page(page)
	except (PageNotAnInteger, TypeError):
		comics = paginator.page(1)
	except EmptyPage:
		comics = paginator.page(paginator.num_pages)

	return render(request, 'comics/comic_archive.html', context = {'filter': comic_filter, 'comics': comics})	

""" View_archive  Attempt 1 
def view_archive(request, page =1):
	allComicPanels = ComicPanel.objects.all().order_by("-uploadTime")
	
	# TODO: Create this
	form = ArchiveSearchForm()
	if request.method == 'POST':
		sortByList = []

		if settings.DEBUG:
			print("Posting on Archive search form!")

		form = ArchiveSearchForm(request.POST)
		# TODO: Work on this form!
		if form.is_valid():

			chapter = form.cleaned_data.get("chapter")
			
			# Filter by chapter
			if chapter:
				allComicPanels = allComicPanels.filter(chapter=chapter)

			# Filter by Tag
			series_number = form.cleaned_data.get("series")

			if settings.DEBUG:
				print("Valid form; series = " + str(getSeriesNames(series_index = series_number)) )

			if series_number and series_number != '0':
				allComicPanels = allComicPanels.filter(series=getSeriesNames(series_index = series_number))

			# Order by
			if form.cleaned_data.get("ascending") == True:
				allComicPanels = allComicPanels.order_by("uploadTime")

				#page = 1

	paginator = Paginator(allComicPanels, 8)  
	try:
		comics = paginator.page(page)
	except PageNotAnInteger:
		comics = paginator.page(1)
	except EmptyPage:
		comics = paginator.page(paginator.num_pages)

	return render(request, 'comics/comic_archive.html',context = {
			'comics': comics,
			'form': form,
			'cur_page': page
			})
"""

# View for specific comic
def view_panel(request, comic_pk =-1 ):

	if request.method == 'GET':
		# Default values for local variables
		comic_panel = None
		newest_comic_pk = -1
		oldest_comic_pk = -1
		next_comic_pk = -1
		prev_comic_pk = -1
		try:
			comic_panel = ComicPanel.objects.all().get(pk=comic_pk)
		except ObjectDoesNotExist:
			return render(request, 'comics/comic_panel_view.html', context = {'comic_panel': comic_panel, 'newest_comic_pk': newest_comic_pk, 'oldest_comic_pk': oldest_comic_pk,
										'prev_comic_pk' : prev_comic_pk,
										'next_comic_pk': next_comic_pk,
									  },) 
			


		# Get chapters
		chapter_dicts = ComicPanel.objects.filter(series = comic_panel.series).values('chapter').distinct()
		chapters = []
		for item in chapter_dicts:
			if item['chapter']:
				chapters.append(item['chapter'])         

		# If Chapters exists
		if chapters:



			finalChapter = max(chapters)
			newest_comic_pk = ComicPanel.objects.filter(
				series = comic_panel.series, 
				chapter=finalChapter).order_by(F("episode").desc(nulls_last=True)).first().pk


			firstChapter = min(chapters)
			oldest_comic_pk = final_comic = ComicPanel.objects.filter(
				series = comic_panel.series, chapter=firstChapter).order_by(F("episode").asc(nulls_last=True)).first().pk

			# Do we have an episode? Find the next, previous and first
			if comic_panel.episode:

				# Is the next episode in the current chaper?
				if ComicPanel.objects.filter(series = comic_panel.series, chapter=comic_panel.chapter, episode = comic_panel.episode+1).exists():
					next_comic_pk = ComicPanel.objects.all().get(
							series=comic_panel.series, chapter=comic_panel.chapter, episode=comic_panel.episode + 1).pk 
					
				# Is the next episode in another chaper?
				elif comic_panel.chapter +1 in chapters:
					next_comic_pk = ComicPanel.objects.all().get(
						series = comic_panel.series,
						chapter = comic_panel.chapter+1, 
						episode = ComicPanel.objects.filter(
							chapter = comic_panel.chapter +1).order_by(F("episode").asc(nulls_last=True)).first().episode).pk
						
				# Is the previous episode in the current chapter?
				if ComicPanel.objects.filter(series = comic_panel.series, chapter=comic_panel.chapter, episode = comic_panel.episode -1).exists():
					prev_comic_pk = ComicPanel.objects.all().get(
						series = comic_panel.series, 
						chapter=comic_panel.chapter, 
						episode = comic_panel.episode -1).pk

				# Is the previous episode in the previous chapter?
				elif comic_panel.chapter -1 in chapters:

					#Find the last episode in the previous chapter  
					prev_comic_pk = ComicPanel.objects.all().get(
						series = comic_panel.series,
						chapter=comic_panel.chapter -1, 
						episode=ComicPanel.objects.filter(
							chapter = comic_panel.chapter -1).order_by(F("episode").desc(nulls_last=True)).first().episode).pk
				

		return render(request, 'comics/comic_panel_view.html',
					context = {'comic_panel': comic_panel,
										'newest_comic_pk': newest_comic_pk,
										'oldest_comic_pk': oldest_comic_pk,
										'prev_comic_pk' : prev_comic_pk,
										'next_comic_pk': next_comic_pk,
									  },)
