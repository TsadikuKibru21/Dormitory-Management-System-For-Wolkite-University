from django.urls import path,include
from .import views

urlpatterns = [
    path('', views.home, name="supervisor"),
    path('assign_block/',views.assign_Block,name='assign_block'),
    path('proctor_info/', views.proctor_Info,name="proctor_info"),
    path('set_schedule/', views.set_schedule,name="set_schedule"),
    path('schedule_info/', views.schedule_info,name="schedule_info"),
    path('update_proctor_block/<str:pk>/', views.update_Proctor_block,name="updateproctorblock"),
    path('delete_proctor_block/<str:pk>/', views.delete_Proctor_block,name="deleteproctorblock"),
    path('export_proctor_schedule/', views.export_proctor_schedule,name="export_proctor_schedule"),
    path('password/',views.PasswordsChangeView.as_view(),name='supervisor_change_paassword'), 
    ############Message########
    path('',include('chat.urls')),

    # path('status/', views.status, name='status'),
   
    path('logout/',views.logout_View,name='logout'),
]