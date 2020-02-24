
from django.shortcuts import render


def error_404(request, exception = None, template = 'error_404.html'):
	return render(request, template, exception)

def privacy_policy(request):
	return render(request, "privacy_policy.html", context = {})

def privacy_policy_source(request):
	return render(request, "privacy_policy_source.html", context = {})