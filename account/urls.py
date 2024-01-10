from django.urls import path,include
from .import views
from .views import PasswordsChangeView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    
    path('',views.adminhome, name='LAdmin'),
    path('update_setting/',views.update_setting, name="update_setting"),
    path('useraccount/',views.generateuseraccount,name="useraccount"),
    path('accountmanagment/',views.accountmanagment,name='accountmanagment'),
    path('account_activate_deactivate',views.account_activate_deactivate,name="account_activate_deactivate"),
    path('Aadduser/', views.AddUser,name="Ad_adduser"),
    path('userinfo/',views.userinfo,name="userinfo"),
    path('deleteuser/',views.deleteuser,name="deleteuser"),
    path('grantrole/', views.GrantRole, name="grantrole"),
    path('updaterole/<int:pk>/',views.updaterole,name='updaterole'),
    path('export_users_csv/', views.export_users_csv,name="export_users_csv"),
    path('password/',PasswordsChangeView.as_view(),name='admin_change_paassword'), 
    # path('password/',auth_views.PasswordChangeView.as_view(template_name='account/change_password.html'),name='admin_change_paassword'),
    #  path('password/',PasswordsResetView.as_view( template_name='account/reset_password.html'),name='password_reset'),
    #path('updateblock/<int:pk>/',views.updateblock,name='updateblock'),PasswordsChangeView
    path('password_reset',views.reset_password,name='password_reset'),
    path('chat/',include('chat.urls')),
    path('logout/',views.logout_View,name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
