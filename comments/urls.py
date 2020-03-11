from django.urls import path
from . import views

app_name = "comments"
urlpatterns = [
    path('comics/<int:comic_pk>/<int:page>/', views.view_comic_comments, name = 'view_comic_comments')
   ,path('post/<int:post_pk>/<int:page>/', views.view_post_comments, name = 'view_post_comments')

]


