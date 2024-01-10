from django.contrib import admin

# Register your models here.
from.models import Borrow_Request,Material,Properties,Exit_Permission,Exit_Permission_Requst

admin.site.register(Borrow_Request)
admin.site.register(Material)
admin.site.register(Properties)
admin.site.register(Exit_Permission)
admin.site.register(Exit_Permission_Requst)