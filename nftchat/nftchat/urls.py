from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import accounts.views 
import mint.views
import chat.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',accounts.views.login, name='login'),
    path('signup/',accounts.views.signup, name='signup'),
    path('logout/',accounts.views.logout, name='logout'),
    path('main/',include('main.urls')),
    path('main/',include('chat.urls')),
    path('mint/',include('mint.urls')),
    path('trade/',mint.views.trade, name = 'trade'),
    path('approval/',mint.views.approval, name = 'approval'),
    path('history/',mint.views.history, name = 'history'),
    path('approval/<int:Token_id>/',mint.views.transfer, name = 'transfer'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

 