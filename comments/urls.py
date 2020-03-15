from django.urls import path
from . import views

app_name = "comments"
urlpatterns = [
    path('comics/<int:comic_pk>/<int:page>/', views.view_comic_comments, name = 'view_comic_comments')
   ,path('post/<int:post_pk>/<int:page>/', views.view_post_comments, name = 'view_post_comments')
   ,path('view_conversations/<int:comment_pk>/<int:cur_set>/', views.view_conversations, name = 'view_conversations')
   ,path('view_conversations/<int:comment_pk>/', views.view_conversations, name = 'view_conversations')
   ,path('delete_comment/<int:comment_pk>/',views.delete_comment, name = 'delete_comment')
   ,path('like_comment/<int:comment_pk>/',views.like_comment, name = 'like_comment')

]


