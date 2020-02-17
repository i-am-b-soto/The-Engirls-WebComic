from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='comic_index'),
    path('<int:comic_pk>/',views.view_panel, name ='view_panel'),
    path('archive/', views.view_archive, name = 'view_archive'),
    path('comments/<int:comic_pk>/<int:page>/', views.view_comments, name = 'view_comments')
]

