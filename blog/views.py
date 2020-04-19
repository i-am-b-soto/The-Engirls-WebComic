from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from comments.forms import CommentForm
from .models import Post #, Comment
from .filters import PostFilter
from django.http import HttpResponse, Http404
from django.conf import settings

###########################################################################
# Blog Views
###########################################################################


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
	post_list = Post.objects.all()
	post_filter = PostFilter(request.GET, queryset=post_list)
	paginator = Paginator(post_filter.qs, settings.BLOG_POST_PAGINATION_COUNT )

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
