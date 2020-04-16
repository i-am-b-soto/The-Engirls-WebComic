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

def get_recepients():
	subscriptions = Subscription.objects.all()
	emails = []
	for sub in subscriptions:
		emails.append(sub.email)
	return emails

	#return ['my_dream1817@hotmail.com', 'iambriansoto@gmail.com', 'kungfunub@gmail.com','theengirlswebcomic@gmail.com' ]
	#return ['iambriansoto@gmail.com']

"""

"""
# Each email 
def send_mass_html_mail(email_template, subject, content, fail_silently=False, user=None, password=None, 
                        connection=None):
    """

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



"""
	Send Thank you Email. 

	Using email_Thanks.html with content name EMAIL_THANKS_CONTENT
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
	