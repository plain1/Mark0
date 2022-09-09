from django.urls import path
from . import views
from .views import(send_friend_request, cancel_friend_request, decline_friend_request, confirm_friend_request, unfriend, friend_requests, friendlists)

urlpatterns = [
    path('', views.main, name='main'),
    path('profiles', views.profiles, name='profiles'),
    path('market', views.market,  name='market'),
    path('chatlists', views.chatlists, name='chatlists'),
    path('friendlists/', friendlists, name='friendlists'),
    path('friendlists/friend_request/',views.send_friend_request ,  name='friend_request'),
    path('friendlists/cancel_friend_request/',views.cancel_friend_request ,  name='cancel_friend_request'),
    path('friendlists/decline_friend_request/',views.decline_friend_request ,  name='decline_friend_request'),
    path('friendlists/confirm_friend_request/',views.confirm_friend_request ,  name='confirm_friend_request'),
    path('friendlists/unfriend/',views.unfriend ,  name='unfriend'),
    path('friendlists/friend_requests/<int:Signup_id>',views.friend_requests ,  name='friend_requests'),
    #path('makechat',views.makechat, name='makechat'),
]