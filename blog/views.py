from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from comments.forms import CommentForm
from .models import Post, Comment
from .filters import PostFilter
from django.http import HttpResponse, Http404

###########################################################################
# Blog Views
###########################################################################

"""
Deprecated
# Load our comments
def view_comments(request, post_pk =-1, page=1):
	comments_paginated = []

	try:
		p = Post.objects.all().get(pk=post_pk)
	except ObjectDoesNotExist as e: 
		raise Http404

	if request.method == 'POST' and request.user.is_authenticated:
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.Post = p
			# Save the comment to the database
			new_comment.name = request.user.username

			new_comment.save()

		else:
			if settings.DEBUG:
				print("Comment form is not valid! HACKER!!! HACKKERRRR!")

	comments = p.comments.all().order_by("-created_on")

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

	return render(request, "comments.html", context = {'comments': comments_paginated, 'post_pk': post_pk } );
"""
class Counter():
	_counter = 0
	def increment(self):
		_counter = _counter +1
	def decrement(self):
		_counter = _counter -1
	def count(self):
		return self._counter

# View post list
def view_posts(request):
	post_list = Post.objects.all().order_by("created_on")
	post_filter = PostFilter(request.GET, queryset=post_list)
	paginator = Paginator(post_filter.qs, 5)

	page = request.GET.get('page', 1)
	try:
		posts = paginator.page(page)
	except (PageNotAnInteger, TypeError):
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'blog/view_posts.html', context = {'filter': post_filter, 'posts': posts, 'counter': Counter()})	

# View individual post
def view_post(request, post_pk =-1):
	p = None
	comment_form = None
	if request.method == 'GET':

		try:
			p = Post.objects.all().get(pk=post_pk)
		except ObjectDoesNotExist as e: 
			raise Http404

		comment_form = CommentForm()
	return render(request, "blog/view_post.html", context = {'post': p, 'comment_form':comment_form} )
