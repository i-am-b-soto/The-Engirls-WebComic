
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ComicPanel
from .models import Tag
#from .forms import ArchiveSearchForm
from django.template import loader, RequestContext
from django.conf import settings
from django.db.models import F
#TODO: might need a template loader


# View for most recent comic
def index(request):
	
	if request.method == 'GET':
	# Let's find the most recent comic!
		chapter_dicts = ComicPanel.objects.values('chapter').distinct()
		chapters = []
		for item in chapter_dicts:
			if item['chapter']:
				chapters.append(item['chapter'])

		#print(chapters)
		if not chapters:
			if settings.DEBUG:
				with open(settings.DEBUG_LOG, 'a') as log:
					log.write(datetime.now().strftime("%d-%m-%Y") + "404 Error thrown in comics.index chapters = " + chapters + "\n")
			raise Http404("I didn't find anything, are there any comics uploaded?")

		finalChapter = max(chapters)
		final_comic = ComicPanel.objects.filter(chapter=finalChapter).order_by(F("episode").desc(nulls_last = True)).first()

		if not final_comic:
			if settings.DEBUG:
				with open(settings.DEBUG_LOG, 'a') as log:
					log.write(datetime.now().strftime("%d-%m-%Y") + "404 Error thrown in comics.index final_comic = " + final_comic + "")
			raise Http404("I didn't find anything, are there any comics uploaded?")

		return view_panel(request, final_comic.pk) 


#class TagAutocomplete(autocomplete.Select2ListView):
"""
	def get_list(self):
		qs = Tag.objects.all()
		tag_names = []
		if self.q:
			qs = qs.filter(text__istartswith=self.q)

		for tagy in qs:
			if (tagy.text) not in tag_names:
				tag_names.append(tagy.text)  

		return tag_names
"""

# View all Comics, sort by... something
def view_archive(request, page =1):
	pass
"""
	allComicPanels = ComicPanel.objects.all().order_by("-uploadTime")
	alltags = Tag.objects.all()	
	# TODO: Create this
	form = ArchiveSearchForm()
	if request.method == 'POST':
		sortByList = []

		form = ArchiveSearchForm(request.POST)
		if form.is_valid():

			# Order by
			if form.cleaned_data.get("ascending") == True:
				allComicPAnels = ComicPanels.order_by("uploadTime")

			# Find by vr
			if form.cleaned_data.get(
					"visual_range") != "" and form.cleaned_data.get("visual_range") != 0:
				allpictures = find_pictures_vr(
					form.cleaned_data.get("visual_range"), allpictures)
				print(form.cleaned_data.get("visual_range"))
				#page = 1

			# Find by date (beginning)
			if form.cleaned_data.get("date1") != "":
				d = datetime.strptime(
					form.cleaned_data.get("date1"), "%m/%d/%Y")
				allpictures = allpictures.filter(uploadTime__gte=d)
				#page = 1

			# Find by date (end)
			if form.cleaned_data.get("date2") != "":
				d = datetime.strptime(
					form.cleaned_data.get("date2"), "%m/%d/%Y")
				allpictures = allpictures.filter(uploadTime__lte=d)
				#page = 1

			# Find by location (must be last since function returns a list)
			if form.cleaned_data.get("location") != "":
				allpictures = find_pictures_tag(
					form.cleaned_data.get("location"), allpictures, alltags)
				#page = 1

	paginator = Paginator(allpictures, 24)  # Show 12 per page
	try:
		pictures = paginator.page(page)
	except PageNotAnInteger:
		pictures = paginator.page(1)
	except EmptyPage:
		pictures = paginator.page(paginator.num_pages)

	# Tell the tag db to get alist of tags from the picture
	tags = []
	computed_vrs = []

	return render(request,
		'comics/comic_archive.html',context = {
			'pictures': pictures,
			'form': form,
			'tags': tags,
			'computed_vrs': computed_vrs})
"""

# function to order the pictures based off the form value
def order_pictures(x, pictures):
	return {
		'0': pictures.order_by("-uploadTime"),
		'1': pictures.order_by("uploadTime"),
		'2': pictures.order_by("eVisualRange"),
		'3': pictures.order_by("-eVisualRange"),
	}[x]    

# Find pictures by tag, warning, returns a list of pictures
# as opposed to a picture object
def find_pictures_tag(location, pictures, alltags):
	pass
"""

	foundpictures = []
	checkpictures = []
	alltags = alltags.filter(text__startswith=location)

	# Convert pictures into a list
	for picture in pictures:
		for tag in alltags:
			if(tag.picture == picture):
				foundpictures.append(picture)

	return foundpictures
"""

# View for specific comic
def view_panel(request, comic_pk =-1 ):
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
