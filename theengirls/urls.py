"""theengirls URL Configuration

"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from content import views as content_views, one_time_load

one_time_load.load_default_content()

urlpatterns = [
	path('', content_views.landing_page, name = "landing_page") # Home URL
	,path('comics/', include('comics.urls')) # comic app URLS
	,path('blog/',include('blog.urls')) # blog URLS
    ,path('comments/', include('comments.urls')) # comment URLS
    ,path('content/',include('content.urls')) # content URLS
    ,path('subscriptions/', include('subscriptions.urls')) # subscription URLS
	,path('admin/', admin.site.urls) # Django Admin URLS
    ,path('accounts/', include('django.contrib.auth.urls')) # Django User Auth URLS
    ,path('oauth/', include('social_django.urls', namespace='social'))  # Social App URLS 
    ,path('ckeditor/', include('ckeditor_uploader.urls')) # CK Editor
    ,path('privacy_policy/', views.privacy_policy, name = "privacy_policy")
    ,path('privacy_policy_source/', views.privacy_policy_source, name = "privacy_policy_source")
    ,path('logout/', views.logout_page, name="custom_logout")
    #,path('about/', about_page, name= "about")
    #,path('about_source/', about_source, name= "about_source")
    #,path('meet_the_engirls/', meet_the_engirls, name = "meet_the_engirls")
    #,path('meet_the_engirls_source/', meet_the_engirls_source, name = "meet_the_engirls_source")


]  
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Media Files
#urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

#handler404 = error_404