from pyexpat import model
from django.db import models
from account.models import User, UserAccount,BlockType
# Create your models here.

PURPOSE= [
    ('Males Block', 'Males Block'),
    ('Females Block', 'Females Block'),
    ]
CHOICES = [
        ('Active', 'Active'),
        ('InActive', 'InActive'),
    ]
Gend=[
    ('Male','Male'),
    ('Female','Female'),
]
Floor=[
    ('Floor-1','Floor-1'),
    ('Floor-2','Floor-2'),
    ('Floor-3','Floor-3'),
    ('Floor-4','Floor-4'),
    ('Floor-5','Floor-5'),
    ('Floor-6','Floor-6'),
    ('Floor-7','Floor-7'),
]

class Block(models.Model):
    Block_name=models.CharField(max_length=100)
    Block_type=models.ForeignKey(BlockType,on_delete=models.CASCADE)
    Block_purpose=models.CharField(max_length=100, choices=PURPOSE) 
    Block_Capacity=models.IntegerField() 
    Status=models.CharField(max_length=150 , choices=CHOICES)
    def __str__(self):
        return self.Block_name
class Dorm(models.Model):
    Block=models.ForeignKey(Block,on_delete=models.CASCADE)
    Dorm_name=models.CharField(max_length=100)
    Floor=models.CharField(max_length=100,choices=Floor)
    Capacity=models.CharField(max_length=10)
    Status=models.CharField(max_length=150 , choices=CHOICES)
    def __str__(self):
        return self.Dorm_name
    

class Placement(models.Model):
    Stud_id=models.ForeignKey(User,on_delete=models.CASCADE)
    Block=models.ForeignKey(Block,on_delete=models.CASCADE)
    Room=models.ForeignKey(Dorm,on_delete=models.CASCADE)
    def __str__(self):
        return self.Stud_id
    
class Announcement(models.Model):
    Title=models.CharField(max_length=100,null=True)
    Content=models.TextField(max_length=3000,null=True,blank=True)
    File=models.FileField(upload_to='files/',null=True,blank=True)
    Active_Date=models.DateField(auto_now=False,auto_now_add=False)
    End_Date=models.DateField(auto_now=False,auto_now_add=False)



class AnnouncementStatus(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)