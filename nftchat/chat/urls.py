from django.urls import path
from . import views

app_name = 'chat' 
urlpatterns = [
    path('makechat/<int:Token_id>/', views.chatroom, name='chatroom'),
    path('enter_room/',views.enter_room, name = 'enter_room'),
    path('search/', views.search, name='search'),
]   