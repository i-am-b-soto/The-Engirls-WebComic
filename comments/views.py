from django.shortcuts import render
from comics.models import ComicPanel
from blog.models import Post
from .models import Comment, Comment_Like
from .forms import CommentForm, ReplyForm
from django.http import HttpResponse, HttpResponseBadRequest, Http404, JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


# Handles Posts to Blog comments and views
def view_post_comments(request, post_pk=-1, page=1):
	comments_paginated = []
	reply_form = ReplyForm()

	try:
		p = Post.objects.all().get(pk=post_pk)
	except ObjectDoesNotExist as e:
		#print("fuck") 
		raise Http404

	if request.method == 'POST' and request.user.is_authenticated:
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.Post = p
			# Save the comment to the database
			new_comment.user = request.user

			new_comment.save()

			return HttpResponse("Success")
		else:
			if settings.DEBUG:
				print("Comment form is not valid! HACKER!!! HACKKERRRR!")
			return HttpResponseBadRequest("bad request processing comment")
	
	if request.method == 'POST' and not request.user.is_authenticated:
		return HttpResponseForbidden("Cannot post comment without login")
		
	comments = p.post_comments.all()

	# Show 5 per page
	paginator = Paginator(comments, settings.COMMENTS_PER_PAGE)

	try:
		comments_paginated = paginator.page(page)
	except PageNotAnInteger:
		comments_paginated = paginator.page(1)
	except EmptyPage:
		comments_paginated = paginator.page(paginator.num_pages)
	except Exception as e:
		print(e)

	return render(request, "comments/comments.html", context = {'comments': comments_paginated, 'reply_form':reply_form } );	

"""
	Delete a comment

	request must:
		1) Must have valid comment object pk
		2) Must be post request
		3) Must have an authenticated user
		4) Must have an authenticated user that matches the comment's user
"""

def delete_comment(request, comment_pk =-1):
	try: 
		comment = Comment.objects.all().get(pk=comment_pk)
	except ObjectDoesNotExist as e:
		if settings.DEBUG:
			print("You fucked up with the comment pk")
		raise Http404

	if request.method == 'POST' and request.user.is_authenticated:
		if comment.user != request.user:
			return HttpResponseForbidden("Authenticated user does not match object user")
		
		comment.delete()

		return HttpResponse("Successfully deleted comment")

	elif request.method == 'POST' and not request.user.is_authenticated:
		return HttpResponseForbidden("User is not authenticated")

	elif request.method is not 'POST':
		return HttpResponseBadRequest("Bad request")



# View the replies in a comment, Post a comment
@ensure_csrf_cookie
def view_conversations(request, comment_pk=-1, cur_set = 1 ):
	reply_form = None 
	replies = []
	retreived_all = True

	try:
		comment = Comment.objects.all().get(pk=comment_pk)
	except ObjectDoesNotExist as e:
		raise Http404

	if request.method == 'GET':
		num_to_retreive = cur_set * 3
		total_replies = comment.comment_comments.all().count()
		
		if num_to_retreive >= total_replies:
			num_to_retreive = total_replies
			retreived_all = True
		else:
			retreived_all = False

		replies = comment.comment_comments.all()[:num_to_retreive]
		

		return render(request, "comments/replies.html", context = {
			'replies':replies, 
			'comment_pk': comment_pk, 
			'cur_set': cur_set, 
			'retreived_all' : retreived_all 
			})


	if request.method == 'POST' and request.user.is_authenticated:

		#if settings.DEBUG:
		#	print("I made it to the post") 

		reply_form = ReplyForm(request.POST)
		if reply_form.is_valid():
			new_reply = reply_form.save(commit=False)
			new_reply.Comment = comment 
			new_reply.user = request.user 
			new_reply.save()

			# Updated comment
			comment.updated_on = timezone.now()
			comment.save()

			# On success 
			return HttpResponse("Successfully created a new reply!") 

		# If form is not valid
		else:
			return HttpResponseBadRequest("Issue processing reply")

	# If user is not authenticated
	if request.method == 'POST' and not request.user.is_authenticated:
		return HttpResponseForbidden("Cannot post comment without login")




# Handles comic panel comment view and posts to comments
def view_comic_comments(request, comic_pk =-1, page=1):
	comments_paginated = []
	reply_form = ReplyForm()


	try:
		cp = ComicPanel.objects.all().get(pk=comic_pk)
	except ObjectDoesNotExist as e: 
		raise Http404

	if request.method == 'POST' and request.user.is_authenticated:

		comment_form = CommentForm(request.POST)
		
		if settings.DEBUG:
			print("Comment Form Errors: " + str(comment_form.errors))
		if comment_form.is_valid():

			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.ComicPanel = cp
			# Save the comment to the database
			new_comment.user = request.user

			new_comment.save()

			return HttpResponse("Success!")

		else:
			if settings.DEBUG:
				print("Comment form is not valid! HACKER!!! HACKKERRRR!")

			return HttpResponseBadRequest("bad request processing comment")

	if request.method == 'POST' and not request.user.is_authenticated:
		return HttpResponseForbidden("Cannot post comment without login")

	comments = cp.comic_panel_comments.all()

	paginator = Paginator(comments, settings.COMMENTS_PER_PAGE)

	try:
		comments_paginated = paginator.page(page)
	except PageNotAnInteger:
		comments_paginated = paginator.page(1)
	except EmptyPage:
		comments_paginated = paginator.page(paginator.num_pages)
	except Exception as e:
		print(e)

	return render(request, "comments/comments.html", context = {'comments': comments_paginated ,'reply_form':reply_form} );
