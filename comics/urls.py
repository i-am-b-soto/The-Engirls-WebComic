from django.urls import path

from . import views
#from .views import TagAutocomplete

urlpatterns = [
	#Path(route, view: httpRequest, kwargs, name)
    path('', views.index, name='index'),
    path('<int:comic_pk>/',views.view_panel, name ='view_panel'),
    path('archive/', views.view_archive, name = 'archive')
    #,path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete')
]