
from django.shortcuts import render


def error_404(request, exception = None, template = 'error_404.html'):
	return render(request, template, exception)