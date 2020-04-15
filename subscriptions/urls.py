from django.urls import path
from . import views

app_name = "subscriptions"
urlpatterns = [
    path('test', views.test, name='test')
    ,path('test2', views.test2, name= 'test2')
    ,path('submit_subscription/', views.submit_subscription, name = 'submit_subscription')
]