
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name="student"),
    path('viewdorm',views.viewdorm,name='viewdorm'),
    path('requests/',views.request_material,name='requests'),
    
    path('my_materials/',views.my_Materials,name='my_materials'),
    path('exit_permission/',views.exit_permission,name='exit_permission'),
    path('Exiteresponse/',views.exit_permission_response,name='Exiteresponse'),
    # path('decline_request/<int:pk>/',views.decline_request,name='decline_request'),
    # path('paassword/',auth_views.PasswordChangeView.as_view(template_name='Student/change_password.html'),name='Std_change_paassword'),
    path('view_announce1/<int:pk>/',views.view_announce1,name='view_announce1'),
    path('view_announcement',views.view_announcement,name='view_announcement'),
    path('paassword/',views.PasswordsChangeView.as_view(template_name='Student/change_password.html'),name='Std_change_paassword'),
    path('reportProblem',views.reportProblem,name='reportProblem'),
    path("approve_problem/<int:pk>/",views.approve_problem,name='approve_problem'),
    path('logout/',views.logout_View,name='logout'),
]