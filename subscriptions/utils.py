from django.conf import settings
import random
import string
from .models import Subscription 
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import SubscriptionForm 
from content.models import Content
from django.http import HttpResponse, HttpResponseBadRequest, Http404, JsonResponse, HttpResponseForbidden 
from django.core.mail import send_mail
from django.core.mail import get_connection, EmailMultiAlternatives

"""
	get_recepients

	Return:
	- list of tuples (email, key)
"""
def get_recepients():
	subscriptions = Subscription.objects.all()
	data_tuples = []
	for sub in subscriptions:
		data_tuples.append((sub.email, sub.key))
	return data_tuples

	#return ['my_dream1817@hotmail.com', 'iambriansoto@gmail.com', 'kungfunub@gmail.com','theengirlswebcomic@gmail.com' ]
	#return ['iambriansoto@gmail.com']

"""
	Send a mass html email...
"""
def send_mass_html_mail(email_template, subject, content, title = None, fail_silently=False, user=None, password=None, 
						connection=None):
	"""

	"""
	recepients = get_recepients()
	datatuple = []
	for email_address, key in recepients:
		# 1) Create the context
		context = {}
		if title:
			context["title"] = title
		context["content"] = content
		context["email_address"] = email_address
		context["key"] = key
		context["domain"] = settings.DOMAIN
		
		# 2) Create HTML + text message
		html_message = render_to_string(email_template, context = context)
		text_message = strip_tags(html_message)

		# 3) Our datatuple
		datatuple.append((subject,text_message, html_message, settings.EMAIL_HOST_USER, [email_address]))

	# 4) Create our connection
	connection = connection or get_connection(
		username=user, password=password, fail_silently=fail_silently)

	# 5) Send our messages
	messages = []
	for subject, text, html, from_email, recipient in datatuple:
		message = EmailMultiAlternatives(subject, text, from_email, recipient)
		message.attach_alternative(html, 'text/html')
		messages.append(message)
	
	# 6) Try to send duh messages
	try:
		connection.send_messages(messages)
	except Exception as e:
		print(str(e))
		print(" A problem sending one or more emails")
		return False
	return True

""" 
	send_new_comic_email
		Send a email for new comic_release

	Input: 
		str title: the title of the comic to release
	Retur: 
		None
"""
def send_new_comic_email(title):
	try:
		subject =  settings.NEW_COMIC_EMAIL_SUBJECT.format(title = title)
	except Exception as e:
		print("Unable to form subject line")
		print(str(e))
		subject = settings.NEW_COMIC_EMAIL_SUBJECT

	content = None
	try:
		content = Content.objects.get(title = settings.CONTENT_KEY_NAMES.get('EMAIL_NEW_COMIC_NAME', None))
	except Content.DoesNotExist as d:
		prnt(str(d))

	send_mass_html_mail("email_new_comic.html",subject, content, title = title, fail_silently = True)
	

"""
	Send Thank you Email. 

	Input:
		str email_address: the email address to send the thank you email to
	Return:
		None

"""
def send_thank_you(email_address):
	subject = settings.THANK_YOU_EMAIL_SUBJECT
	try:
		content = Content.objects.get(title = settings.CONTENT_KEY_NAMES.get('EMAIL_THANKS_CONTENT_NAME', None))
	except Content.DoesNotExist:
		print("Could not find content with tite: ".format(settings.CONTENT_KEY_NAMES.get('EMAIL_THANKS_CONTENT_NAME')))

	key = None

	# Retreive key associated with email 
	try:
		sub = Subscription.objects.get(email = email_address)
	except Subsription.ObjectDoesNotExist as d:
		print(str(d))
		return False
	key = sub.key

	html_message = render_to_string('email_thanks.html', context = {"content":content, "key":key, "email_address": email_address, "domain":settings.DOMAIN})
	regular_message = strip_tags(html_message)
	from_email = settings.EMAIL_HOST_USER	# Email 
	to_email = email_address
	try: 
		send_mail( 
			subject,
			regular_message,
			from_email,
			[to_email],
			fail_silently=True,
			html_message = html_message,
		)
	except Exception as e:
		print("Unable to send email")
		print(str(e))
		return False
	return True

"""

"""
def send_update_email():
	pass


"""
	Generate a random string
"""
def randomString(stringLength=10):
	"""Generate a random string of fixed length """
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(stringLength))


"""
	Generate a unique key not in Subscription objects
"""
def get_key():
	rs = randomString()
	while Subscription.objects.filter(key = rs).exists():
		# Generate a new random string
		rs = randomString()
	return rs

""" 
	Must be a valid subscription form

	Creates a subscription element with a unique key and email

"""
def create_subscription(subscription_form):
	if not subscription_form.is_valid():
		raise Exception("Subscription form must be valid before calling this method")
	sub = subscription_form.save(commit = False)
	if Subscription.objects.filter(email = sub.email).exists():
		return False 
	sub.key = get_key()
	sub.save()
	# Need to create a key that does not exist
	return True
	