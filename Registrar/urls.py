from django.urls import path,include
from .import views

urlpatterns = [
    # path('LAdmin/',include("account.urls"),name="Admin"),
    # path('admin/', admin.site.urls),
    path('',views.index, name="Registrar"),
    path('logout/',views.logout_View,name='logout'),
    path("download-csv/", views.download_excel, name="download_csv"),
    path('EditStudent/<int:pk>/', views.Edit_Students,name='EditStudent'),
    path('DeleteStudent/<int:pk>/', views.delete_student,name='DeleteStudent'),
    path('adduser/',views.Adduser,name='adduser'),
    path('adduser/adduser1',views.Adduser1,name='adduser1'),
    path('R_viewstudent',views.viewStudent,name='R_viewstudent'),
    path('password/',views.PasswordsChangeView.as_view( template_name='Registrar/change_password.html'),name='registrar_change_paassword'), 

    path('Import_User/',views.Import_User,name="Import_User"),
     ############Message########
    path('',include('chat.urls')),
]