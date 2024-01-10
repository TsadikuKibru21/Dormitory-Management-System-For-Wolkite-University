from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import ActivityLog
def log_insertion(sender,instance,created,**kwargs):
    if created:
        ActivityLog.objects.create(user=instance.user,action='insertion')



def log_deletion(sender,instance,**kwargs):
    ActivityLog.objects.create(user=instance.user,action='deletion')



def log_update(sender,instance,created,**kwargs):
    if not created:
        ActivityLog.objects.create(user=instance.user,action='update')
