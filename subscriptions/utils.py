from django.conf import settings
import random
import string
from .models import Subscription 
from .forms import SubscriptionForm 
from django.http import HttpResponse, HttpResponseBadRequest, Http404, JsonResponse, HttpResponseForbidden 

def send_thank_you(email):
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

"""
def create_subscription(subscription_form):
	if not subscription_form.is_valid():
		raise Exception("Subscription form must be valid before calling this method")
	sub = subscription_form.save(commit = False)
	if Subscription.objects.filter(email = sub.email).exists():
		return False 
	key = get_key()
	sub.save()
	# Need to create a key that does not exist
	return True
	