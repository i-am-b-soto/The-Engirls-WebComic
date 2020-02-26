from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect


def error_404(request, exception = None, template = 'error_404.html'):
	return render(request, template, exception)

def privacy_policy(request):
	return render(request, "privacy_policy.html", context = {})

def privacy_policy_source(request):
	return render(request, "privacy_policy_source.html", context = {})

def logout_page(request):
	logout(request)
	return HttpResponseRedirect(request.GET.get('next', '/'))