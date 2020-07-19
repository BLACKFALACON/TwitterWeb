from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns=[
    path('hastagtweet/<hastag>',FilterTweet, name='hastagtweet'),
    path('delete/<int:id>',ClearContact, name='clearcontact'),
    path('',IndexView,name='index'),
    path('analizler/',AnalizView, name='analizler'),
    path('contact/',ContactView, name='contact'),
    path('hesap/',HesapView, name='hesap'), 
    path('analiz/',AnalizEtView, name='analiz'),
    path('analizgöster/',AnalizGöster, name='analizgöster'), 





]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)