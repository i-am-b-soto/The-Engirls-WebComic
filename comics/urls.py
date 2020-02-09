from django.urls import path

from . import views
#from .views import TagAutocomplete

urlpatterns = [
	#Path(route, view: httpRequest, kwargs, name)
    path('', views.index, name='comic_index'),
    #path('/', views.index, name='comic_index2'),
    path('<int:comic_pk>/',views.view_panel, name ='view_panel'),
    path('archive/<int:page>/', views.view_archive, name = 'view_archive'),
    path('archive/', views.view_archive, name = 'view_archive'),
    path('series-autocomplete/', views.SeriesAutocomplete.as_view(), name='series-autocomplete')
]

