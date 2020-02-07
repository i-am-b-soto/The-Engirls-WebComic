
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import ComicPanel
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
		if ComicPanel.objects.filter(series="main").exists():
		

			chapter_dicts = ComicPanel.objects.filter(series="main").values('chapter').distinct()
			chapters = []
			for item in chapter_dicts:
				if item['chapter']:
					chapters.append(item['chapter'])

			if chapters:
				finalChapter = max(chapters)
				comic_to_display = ComicPanel.objects.filter(
					series="main",
					chapter=finalChapter
					).order_by(F("episode").desc(nulls_last = True)).first()
			else:
				comic_to_display = ComicPanel.objects.all().order_by("-uploadedTime").first()

		else:
			comic_to_display = ComicPanel.objects.all().order_by("-uploadedTime").first()
		return view_panel(request, comic_to_display.pk) 




class SeriesAutocomplete(autocomplete.Select2ListView):
	pass
"""
	def get_list(self):
		return list (ComicPanel.objects.values('series_name').distinct())

"""
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
	pass

"""
 if id != -1:

		if request.method == 'GET':
			# Good picture id
			try:
				comic_panel = ComicPanel.objects.all().get(pk=comic_pk)
			except ObjectDoesNotExist:
				raise Http404("I didn't find anything, are there any comics uploaded?")  
			
			# Get chapters
			chapter_dicts = ComicPanel.objects.values('chapter').distinct()
			chapters = []
			for item in chapter_dicts:
				if item['chapter']:
					chapters.append(item['chapter'])

			if not chapters:
				if settings.DEBUG:
					with open(settings.DEBUG_LOG, 'a') as log:
						log.write(datetime.now().strftime("%d-%m-%Y") + "404 Error thrown in comics.index chapters = " + chapters + "\n")

				raise Http404("I didn't find anything, are there any comics uploaded?")            


			finalChapter = max(chapters)
			newest_comic_pk = ComicPanel.objects.filter(chapter=finalChapter).order_by(F("episode").desc(nulls_last=True)).first().pk


			firstChapter = min(chapters)
			oldest_comic_pk = final_comic = ComicPanel.objects.filter(chapter=firstChapter).order_by(F("episode").asc(nulls_last=True)).first().pk


			next_comic_pk = -1
			prev_comic_pk = -1

			
			if comic_panel.episode:

				# Is the next episode in the current chaper?
				if ComicPanel.objects.filter(chapter=comic_panel.chapter, episode = comic_panel.episode+1).exists():
					next_comic_pk = ComicPanel.objects.all().get(chapter=comic_panel.chapter, episode = comic_panel.episode + 1).pk 
				
				# Is the next episode in another chaper
				elif comic_panel.chapter +1 in chapters:
					next_comic_pk = ComicPanel.objects.all().get(
						chapter = comic_panel.chapter+1, 
						episode = ComicPanel.objects.filter(
							chapter = comic_panel.chapter +1).order_by(F("episode").asc(nulls_last=True)).first().episode).pk
					
				# Is the previous episode in the current chapter?
				if ComicPanel.objects.filter(chapter=comic_panel.chapter, episode = comic_panel.episode -1).exists():
					prev_comic_pk = ComicPanel.objects.all().get(chapter=comic_panel.chapter, episode = comic_panel.episode -1).pk

				# Is the previous episode in the previous chapter?
				elif comic_panel.chapter -1 in chapters:

					#Find the last episode in the previous chapter  
					prev_comic_pk = ComicPanel.objects.all().get(
						chapter=comic_panel.chapter -1, 
						episode=ComicPanel.objects.filter(
							chapter = comic_panel.chapter -1).order_by(F("episode").desc(nulls_last=True)).first().episode).pk
				

			# Tell the tag db to get alist of tags from the picture
			tags = Tag.objects.filter(picture=comic_panel)

			return render(request, 'comics/comic_panel_view.html',
				context = {'comic_panel': comic_panel,
										'newest_comic_pk': newest_comic_pk,
										'oldest_comic_pk': oldest_comic_pk,
										'prev_comic_pk' : prev_comic_pk,
										'next_comic_pk': next_comic_pk,
										'tags':tags
									  },)
		else:
			raise Http404("I can't find that page. Bitch, what you tryna do?")
"""