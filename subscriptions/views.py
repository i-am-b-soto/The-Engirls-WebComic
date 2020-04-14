from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from content.models import Content
import random
from .models import Subscription 
from .forms import SubscriptionForm  
from django.http import HttpResponse, HttpResponseBadRequest, Http404, JsonResponse, HttpResponseForbidden

""" 
	* Must be a valid subscription form
"""
def create_subscription(subscription_form):
	if not subscription_form.is_valid():
		raise Exception("Subscription form must be valid before calling this method")
	sub = subscription_form.save(commit = False)
	# Need to create a key that does not exist
	pass

"""

"""
def submit_subscription(request):
	if request.method != 'POST':
		return HttpResponseBadRequest("Must be a POST Request to access this resource")
	subscription_form = subscription_form(request.POST)
	if subscription_form.is_valid():
		create_subscription(subscription_form)
	else:
		return HttpResponseBadRequest("Sorry, didn't quite get that")

	return HttpResponse("Thank You!")

def custom_email(request):
	pass

def newContent(request):
	pass

def unsubscribe(request):
	return HttpResponse("Unsubscribed")

def subscribe(request):
	
	return HttpResponse("Subscribe")


def get_recepients():
	# TODO actually get recipients
	return ['my_dream1817@hotmail.com', 'iambriansoto@gmail.com', 'kungfunub@gmail.com','theengirlswebcomic@gmail.com' ]
	#return ['iambriansoto@gmail.com']

# Each email 
def send_mass_html_mail(email_template, subject, content, fail_silently=False, user=None, password=None, 
                        connection=None):
    """
    Given a datatuple of (subject, text_content, html_content, from_email,
    recipient_list), sends each message to each recipient list. Returns the
    number of emails sent.

    If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
    If auth_user and auth_password are set, they're used to log in.
    If auth_user is None, the EMAIL_HOST_USER setting is used.
    If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

    """
    recepients = get_recepients()
    datatuple = []
    for recepient in recepients:
    	html_message = render_to_string(email_template, context = {"content": content })
    	text_message = strip_tags(html_message)
    	datatuple.append((subject,text_message, html_message, settings.EMAIL_HOST_USER, [recepient]))

    connection = connection or get_connection(
        username=user, password=password, fail_silently=fail_silently)

    messages = []
    for subject, text, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, text, from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)

def test(request):
	subject = 'The Engirls Test3 - Subject'
	html_message = render_to_string('subscriptions/test.html')
	regular_message = strip_tags(html_message)
	from_email = settings.EMAIL_HOST_USER
	to_email = 'my_dream1817@hotmail.com'
	send_mail( 
		subject,
		regular_message,
		from_email,
		[to_email],
		fail_silently=False,
		html_message = html_message,
	)
	return HttpResponse("Test Executed")

def test2(request):
	content = None
	try:
		content = Content.objects.get(title = settings.CONTENT_KEY_NAMES.get('EMAIL_THANKS_CONTENT_NAME', None))
	except Content.DoesNotExist:
		print("Couldn't find the content")	
	
	send_mass_html_mail("subscriptions/thanks.html", "Thanks for Subscribing!", content)
	
	return HttpResponse("Executed Test2")
	
	"""
	html_message = render_to_string("subscriptions/thanks.html", context = {"content": content })
	return HttpResponse(render_to_string(html_message))
	"""