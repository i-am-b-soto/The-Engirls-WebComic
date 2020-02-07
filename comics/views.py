
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import ComicPanel
from django.http import HttpResponse, Http404
#from .models import Tag
from .forms import ArchiveSearchForm
from django.template import loader, RequestContext
from django.conf import settings
from django.db.models import F
from dal import autocomplete

#TODO: might need a template loader


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

class SeriesAutocomplete(autocomplete.Select2ListView):

	def get_list(self):
		return list (ComicPanel.objects.values('series_name').distinct())

""" View_archive """
def view_archive(request, page =1):
	pass
"""
	allComicPanels = ComicPanel.objects.all().order_by("-uploadTime")
	# TODO: Create this
	form = ArchiveSearchForm()
	if request.method == 'POST':
		sortByList = []

		form = ArchiveSearchForm(request.POST)
		if form.is_valid():

			# Order by
			if form.cleaned_data.get("ascending") == True:
				allComicPAnels = ComicPanels.order_by("uploadTime")

			chapter = form.cleaned_data.get("chapter")
			
			# Filter by chapter
			if chapter:
				allpictures = allComicPanels.filter(chapter=chapter)

			# Filter by Tag
			tag = form.cleaned_data.get("tag")
			if tag:
				allpictures = allComicPanels.filter(tag=tag)
				#page = 1

	paginator = Paginator(allComicPanels, 4)  # Show 4 per page
	try:
		comics = paginator.page(page)
	except PageNotAnInteger:
		comics = paginator.page(1)
	except EmptyPage:
		comics = paginator.page(paginator.num_pages)

	return render(request, 'comics/comic_archive.html',context = {
			'comics': comics,
			'form': form})

"""
# View for specific comic
def view_panel(request, comic_pk =-1 ):

 if id != -1:

		if request.method == 'GET':

			try:
				comic_panel = ComicPanel.objects.all().get(pk=comic_pk)
			
			except ObjectDoesNotExist:
				raise Http404("I didn't find anything, are there any comics uploaded?")  
			
			# Default values for local variables
			newest_comic_pk = comic_panel.pk
			oldest_comic_pk = comic_panel.pk
			next_comic_pk = -1
			prev_comic_pk = -1

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
		else:
			raise Http404("I can't find that page. Bitch, what you tryna do?")
