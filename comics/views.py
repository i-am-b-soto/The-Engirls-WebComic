from .forms import CommentForm
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import ComicPanel, Comment
from django.http import HttpResponse, Http404
from django.template import loader, RequestContext
from django.conf import settings
from django.db.models import F
from .filters import ComicPanelFilter

from social_django.models import UserSocialAuth



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

# View Archive
def view_archive(request):

	comic_list = ComicPanel.objects.all().order_by("uploadTime")
	comic_filter = ComicPanelFilter(request.GET, queryset=comic_list)
	paginator = Paginator(comic_filter.qs, 8)

	page = request.GET.get('page', 1)
	try:
		comics = paginator.page(page)
	except (PageNotAnInteger, TypeError):
		comics = paginator.page(1)
	except EmptyPage:
		comics = paginator.page(paginator.num_pages)

	return render(request, 'comics/comic_archive.html', context = {'filter': comic_filter, 'comics': comics})	


# Load our comments
def view_comments(request, comic_pk, page=1):
	comments_paginated = []

	try:
		cp = ComicPanel.objects.all().get(pk=comic_pk)
	except ObjectDoesNotExist as e: 
		raise Http404

	if request.method == 'POST' and request.user.is_authenticated:
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.ComicPanel = cp
			# Save the comment to the database
			new_comment.name = request.user.username

			new_comment.save()

		else:
			if settings.DEBUG:
				print("Comment form is not valid! HACKER!!! HACKKERRRR!")

	comments = cp.comments.all().order_by("-created_on")

	# Show 5 per page
	paginator = Paginator(comments, 10)

	try:
		comments_paginated = paginator.page(page)
	except PageNotAnInteger:
		comments_paginated = paginator.page(1)
	except EmptyPage:
		comments_paginated = paginator.page(paginator.num_pages)
	except Exception as e:
		print(e)

	return render(request, "comics/comments.html", context = {'comments': comments_paginated, 'comic_pk': comic_pk } );


# View for specific comic
def view_panel(request, comic_pk =-1 ):

	comic_panel = None
	newest_comic_pk = -1
	oldest_comic_pk = -1
	next_comic_pk = -1
	prev_comic_pk = -1
	comment_form = CommentForm()

	# Try to get comment with given pk. Return default values otherwise
	try:
		comic_panel = ComicPanel.objects.all().get(pk=comic_pk)
	except ObjectDoesNotExist:
		return render(request, 'comics/comic_panel_view.html', context = {'comic_panel': comic_panel, 'newest_comic_pk': newest_comic_pk, 'oldest_comic_pk': oldest_comic_pk,
									'prev_comic_pk' : prev_comic_pk,
									'next_comic_pk': next_comic_pk,
									'comment_form': comment_form
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
		'comment_form':comment_form
									  })
