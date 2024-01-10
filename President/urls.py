

from django.urls import path,include
from .import views
urlpatterns = [
    path('', views.presidenthome, name="president"),
    path('Permission/', views.give_permission, name="President_givepermission"),
    path('BlockInfo/',views.viewblock,name="President_viewblock"),
    path('DormInfo/<int:pk>/',views.viewdorm,name='President_viewdorm'),
    path('placementinfo/',views.View_placement,name="President_placementinfo"),
    path('overallinfo/',views.OverallInfo,name="overallinfo"),
    path('password/',views.PasswordsChangeView.as_view(),name='president_change_paassword'),
        ############Message########
    path('chat/',include('chat.urls')),
]