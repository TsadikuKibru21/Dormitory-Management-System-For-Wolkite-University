from django.urls import path, include
from . import views

urlpatterns = [
    path("chat/", views.chatindex, name="chatindex"),
    path("search/", views.search, name="search"),
    path("addfriend/<str:name>", views.addFriend, name="addfriend"),
    path("chat/<str:username>", views.chat, name="chat"),
    path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
    path('api/messages', views.message_list, name='message-list'),
    path("home/", views.backpage, name="backtohome"),
]