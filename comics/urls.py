from django.urls import path
from . import views

app_name = "comics"
urlpatterns = [
    path('', views.index, name='comic_index')
    ,path('<int:comic_pk>/',views.view_panel, name ='view_panel')
    ,path('archive/', views.view_archive, name = 'view_archive')
    ,path('comments/<int:comic_pk>/<int:page>/', views.view_comments, name = 'view_comments')
    ,path('auto_complete_chapter/', views.auto_complete_chapter, name = 'auto_complete_chapter')
    ,path('auto_complete_page/', views.auto_complete_page, name = 'auto_complete_page')
]


