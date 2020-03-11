from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
	 path('', views.view_posts, name = 'view_posts')
    ,path('post/<int:post_pk>/', views.view_post, name = 'view_post')
    # ,path('comments/<int:post_pk>/<int:page>/',views.view_comments, name = 'view_comments') --> Deprecated
]


