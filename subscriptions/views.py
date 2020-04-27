from django.shortcuts import render
from django.conf import settings
from content.models import Content
import random
import string
from .models import Subscription 
from .forms import SubscriptionForm  
from django.http import HttpResponse, HttpResponseBadRequest, Http404, JsonResponse, HttpResponseForbidden 
from .utils import create_subscription, send_thank_you
import _thread as thread
from ratelimit.decorators import ratelimit

"""
	Render Subscription form
"""
def subscribe(request):
	
	if request.method != 'GET':
		return HttpResponseBadRequest("Must be a GET request")
	subscription_form = SubscriptionForm()
	return render(request, "subscriptions/subscribe.html", context = {"subscription_form":subscription_form})

"""
	Unsubscribe
"""
@ratelimit(key='ip', rate='10/h', block=True)
def unsubscribe(request, email_address =-1, key =-1):
	email_address = request.GET.get('email_address', None)
	key = request.GET.get('key', None)

	if request.method!= 'GET':
		return HttpResponseBadRequest("Must be a GET request to access this resource")
	sub = None	
	try:
		sub = Subscription.objects.get(email = email_address)
	except Subscription.DoesNotExist:
		return HttpResponseBadRequest("Email address does not exist")

	# Make sure user has the correct key
	if key == sub.key:
		sub.delete()
		content = None
		try:
			content = Content.objects.get(title = settings.CONTENT_KEY_NAMES.get('UNSUBSCRIBE_CONTENT_NAME',None))
		except content.DoesNotExist as d:
			print(str(d))

		return render(request, "Sorry_To_See_You_Leave.html", context = {"content": content})
	# If key does not match
	else: 
		return HttpResponseBadRequest("Looks like you don't have the right key...")


"""
	Submit subscription, with a post request
"""
@ratelimit(key='ip', rate='10/h', block=True)
def submit_subscription(request):
	if request.method != 'POST':
		return HttpResponseBadRequest("Must be a POST Request to access this resource")
	
	if not request.is_secure():
		return JsonResponse({"Response": "Looks like you're not on a secure connection. Try accessing the site through 'https' "})

	subscription_form = SubscriptionForm(request.POST)
	if subscription_form.is_valid():
		if not create_subscription(subscription_form):
			return JsonResponse({"Response":"We already got this email on record!"})
	# If there are errors in the subscription form
	else:
		return JsonResponse({"Response": subscription_form['email'].errors})

	# Try sending email in new thread
	try:
		thread.start_new_thread( send_thank_you, (subscription_form.cleaned_data['email'], ) )
	except Exception as e:
		print("Unable to start new thread-{}".format(str(e)))
		return JsonResponse({"Response": "Internal Server Error. Please try again soon :)"})

	#send_thank_you(subscription_form.cleaned_data['email'])
	return JsonResponse({"Response": "Got it, Thank You!"})

def custom_email(request):
	pass

