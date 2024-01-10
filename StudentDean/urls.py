from django.urls import path,include
from .import views


urlpatterns = [
    path('', views.home, name="studentdeanhome"),
    #########User Managment#####
    path('addemployee',views.addEmployee,name='addemployee'),
    path('S_grantrole',views.grantrole,name="S_grantrole"),
    path('account_activate_deactivate',views.account_activate_deactivate,name="S_account_activate_deactivate"),
    path('S_updaterole/<int:pk>/',views.updaterole,name='S_updaterole'),
    path('S_Import_User/',views.Import_User,name="S_Import_User"),
    path('view_employee/',views.view_employee,name="view_employee"),
    path('S_delete_employee/<int:pk>/',views.delete_employee,name="S_delete_employee"),
    path('S_update_employee/<int:pk>/',views.update_employee,name="S_update_employee"),
    path('blockadd/',views.BlockAdd,name='blockadd'),
    path('addblocktype/',views.blockType,name='addblocktype'),
    path('add_dorm/',views.add_dorm,name="add_dorm"),
    path('viewblock/', views.viewblock, name="viewblock"),
    path('viewdorm/<int:pk>/',views.viewdorm,name='viewdorm'),
    path('updateblock/<int:pk>/',views.updateblock,name='updateblock'),
    path('updatedorm/<int:pk>/',views.updatedorm,name='updatedorm'),
    path('delatedorm/<int:pk>/',views.delatedorm,name='delatedorm'),
    path('delateblock/<int:pk>/',views.delateblock,name='delateblock'),
    path('resetPlacement/',views.resetPlacement,name="resetPlacement"),
    path('delete_placement/',views.delete_placement,name="delete_placement"),
    path('rPlacement/',views.rPlacement,name="rPlacement"),
    path('placestudent/',views.PlaceStudent,name="placestudent"),
    path('managePlacement/',views.managePlacement,name="managePlacement"),
    path('updateStudent/<int:pk>/',views.updateStudent,name='updateStudent'),
    path('export_placement_csv/', views.export_users_csv,name="export_placement_csv"),
    path('delateStudent/<int:pk>/',views.delateStudent,name='delateStudent'),
    path('paassword/',views.PasswordsChangeView.as_view(template_name='StudentDean/change_password.html'),name='Sdean_change_paassword'),
    path('view_announce/<int:pk>/',views.view_announce,name='view_announce'),
    path('announce/',views.announce,name='announce'),
    path('manage_announce/',views.manage_announce,name='manage_announce'),
    path('Edit_Announcement/<int:pk>/',views.Edit_Announcement,name='Edit_Announcement'),
    path('overallinfo/',views.OverallInfo,name="SDoverallinfo"),
     ############Message########
    path('',include('chat.urls')),

    path('logout/',views.logout_View,name='logout'),
]


# from django.urls import path

# from .models import Block
# from .serializers import BlockSerializer 
# from .views import BlockView,BlockAdd,blockadd,add_dorm,add_dorm1,home

# urlpatterns = [
#     path('', home, name="studentdeanhome"),
#     path('blockadd/',BlockAdd,name='blockadd'),
#     path('blockadd/blockadd1',blockadd,name='blockadd1'),
#     path('add_dorm/',add_dorm,name='add_dorm'),
#     path('add_dorm/add_dorm1',add_dorm1,name='add_dorm1'),
#     # path('viewblock/',viewblock,name='viewblock'),
# ]
