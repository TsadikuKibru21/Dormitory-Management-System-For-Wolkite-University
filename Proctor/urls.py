
from django.urls import path,include

from .import views
urlpatterns = [
    path('',views.index, name="proctor"),
    path('borrow_material/',views.borrow_material,name="borrow_material"),
    path("confirm/<int:pk>/",views.confirm_request,name='confirm_request'),
    path("decline_material_request/<int:pk>/",views.decline_material_request,name='decline_material_request'),
    path('Student/',views.student_info,name="Student"),
    path('return_material/<int:pk>/',views.return_material,name='return_material'),
    path('borrowed_materials/<int:pk>',views.borrowed_materials,name='borrowed_materials'),
    #######Materials######
    path('register_material/',views.register_material, name='register_material'),
    path('view_Materials/',views.view_Materials,name='view_Materials'),
    path('edit_Materials/<int:pk>/',views.edit_material,name='edit_material'),
    path('delete_Materials/<int:pk>/',views.delete_material,name='delete_Materials'),
    path('upload_materials/',views.Import_materials,name='upload_materials'),
    path('search_material/',views.search_material,name='search_material'),
    #path("download-csv/", views.DownloadCSVViewdownloadcsv.as_view(), name="download_csv1"),
    path('download_excel',views.download_excel,name='download_csv1'),
    ##########Exit Permission#########
    path('exit_requests/',views.exit_permission_requests,name='exit_requests'),
    path('accept_request/<int:pk>/',views.accept_exit_request,name='accept_exit_request'),
    path('decline_request/<int:pk>/',views.decline_request,name='decline_request'),
    path('password/',views.PasswordsChangeView.as_view(),name='proctor_change_paassword'),
    ###########Problem##############
    path("report_view",views.report_view,name='report_view'),
    path("all_report_view",views.all_report_view,name='all_report_view'), 
    ############Message########
    path('',include('chat.urls')),
]
