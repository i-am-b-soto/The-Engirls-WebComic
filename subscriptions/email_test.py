from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

subject = 'The Engirls Test - Subject'
html_message = render_to_string('subscriptions/test.html')
regular_message = strip_tags(html_message)
from_email = settings.EMAIL_HOST_USER
to_email = 'iambriansoto@gmail.com'
send_mail( 
	subject,
	regular_message,
	from_email,
	to_email,
	fail_silently=False,
	html_message = html_message,
)