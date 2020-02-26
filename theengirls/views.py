from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect


def error_404(request, exception = None, template = 'error_404.html'):
	return render(request, template, exception)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect(request.GET.get('next', '/'))

# Static pages...

def privacy_policy(request):
	return render(request, "privacy_policy.html", context = {})

def privacy_policy_source(request):
	return render(request, "privacy_policy_source.html", context = {})

def about_page(request):
	return render(request, "about.html", context = {})

def about_source(request):
	return render(request, "about_source.html", context = {})

def meet_the_engirls(request):
	return render(request, "meet_the_engirls.html", context ={})

def meet_the_engirls_source(request):
	return render(request, "meet_the_engirls_source.html", context = {})