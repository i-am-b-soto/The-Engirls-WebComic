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
def unsubscribe(request, email_address =-1, key =-1):
	
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
		return render(request, "Sorry_To_See_You_Leave.html")
	# If key does not match
	else: 
		return HttpResponseBadRequest("Something went wrong...")


"""
	Submit subscription, with a post request
"""
@ratelimit(key='ip', rate='5/h', block=True)
def submit_subscription(request):
	if request.method != 'POST':
		return HttpResponseBadRequest("Must be a POST Request to access this resource")
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
	#send_thank_you(subscription_form.cleaned_data['email'])
	return JsonResponse({"Response": "Got it, Thank You!"})

def custom_email(request):
	pass

def newContent(request):
	pass


"""

def test2(request):
	content = None
	try:
		content = Content.objects.get(title = settings.CONTENT_KEY_NAMES.get('EMAIL_THANKS_CONTENT_NAME', None))
	except Content.DoesNotExist:
		print("Couldn't find the content")	
	
	send_mass_html_mail("subscriptions/thanks.html", "Thanks for Subscribing!", content)
	
	return HttpResponse("Executed Test2")
	
"""
"""
	html_message = render_to_string("subscriptions/thanks.html", context = {"content": content })
	return HttpResponse(render_to_string(html_message))
"""