"""theengirls URL Configuration


Add social login:
https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html  

Login with AJAX:
https://stackoverflow.com/questions/35461517/django-registration-ajax-post-form

How Django Authentication works:
https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication

"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import error_404  

urlpatterns = [
	path('', include('comics.urls')), # Home URL
	path('comics/', include('comics.urls')), # Comic app URKS
	path('admin/', admin.site.urls), # Django Admin URLS
    path('accounts/', include('django.contrib.auth.urls')), # Django User Auth URLS
    path('oauth/', include('social_django.urls', namespace='social')),  # Social App URLS 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Media Files

#handler404 = error_404