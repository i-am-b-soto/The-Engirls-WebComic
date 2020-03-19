from django.urls import path
from . import views

app_name = "content"
urlpatterns = [
    path('get_content/', views.get_content, name = 'get_content')
    ,path('<int:content_pk>/',views.content_view, name ='content_view')

]


