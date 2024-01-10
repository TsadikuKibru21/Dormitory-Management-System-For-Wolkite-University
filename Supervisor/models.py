from django.db import models
from account.models import UserAccount
from StudentDean.models import Block
# Create your models here.
class ProctorAssignment(models.Model):
    user=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    Block=models.ForeignKey(Block,on_delete=models.CASCADE)
    
    # time=models.TimeField()
    def __str__(self):
        return self.user
class schedule(models.Model):
    procotor=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    shift=models.CharField(max_length=10,null=False)
    date=models.DateField(null=False)
    num_shift_per_day=models.IntegerField(null=True)
    def __str__(self):
        return self.procotor