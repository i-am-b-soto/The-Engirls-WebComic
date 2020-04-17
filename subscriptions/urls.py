from django.urls import path
from . import views

"""
	Some bitchin URLS
"""
app_name = "subscriptions"
urlpatterns = [
    #path('test', views.test, name='test')
    #,path('test2', views.test2, name= 'test2')
    path('submit_subscription/', views.submit_subscription, name = 'submit_subscription')
    ,path('subscribe/', views.subscribe, name = 'subscribe')
    ,path('unsubscribe/<str:email_address>/<str:key>/', views.unsubscribe, name = 'unsubscribe') 

]