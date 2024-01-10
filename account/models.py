from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class BlockType(models.Model):
    Block_Type=models.CharField(max_length=100)
    def __str__(self):
        return self.Block_Type
class Role(models.Model):
    R_name=models.CharField(max_length=200)
    def __str__(self):
        return self.R_name
class User(models.Model):
    GENDER_CHOICES=(
        ('M','Male'),
        ('F', 'Female')
    )
    stream=(

        ('social','social'),
        ('natural','natural')

    )
    Disability=(
        ('Disable','Disable'),
        ('Not_Disable','Not_Disable')
    )
    #Role=models.ForeignKey(Role,on_delete=models.CASCADE,null=True)
    Id_no=models.CharField(max_length=200,null=False)
    FirstName=models.CharField(max_length=100,null=False)
    LastName=models.CharField(max_length=100,null=False)
    Gender=models.CharField(choices=GENDER_CHOICES, max_length=6, null=False,default='M')
    phone_no=models.CharField(max_length=15,null=False)
    email=models.EmailField(max_length=100,unique=True,null=True,blank=True)
    is_Employee=models.BooleanField(default=False)
    stream=models.CharField(max_length=200, null=True,blank=True,choices=stream,default='nan')
    collage=models.CharField(max_length=200, null=True,blank=True,default='nan')
    Department=models.CharField(max_length=200, null=True,blank=True,default='nan')
    Year_of_Student=models.CharField(max_length=50, null=True,blank=True,default='nan')
    Campus=models.ForeignKey(BlockType,on_delete=models.CASCADE,null=True,blank=True)
    Region=models.CharField(max_length=200,null=True,blank=True)
    Emergency_responder_name=models.CharField(max_length=200,null=True,blank=True)
    Emergency_responder_address=models.CharField(max_length=200,null=True,blank=True)
    Emergency_responder_phone_no=models.CharField(max_length=13, null=True,blank=True)
    Disability=models.CharField(max_length=100,choices=Disability, null=True,blank=True)
    # Employee_id=models.CharField(max_length=50, null=True,blank=True)
    # Student_or_Not=models.CharField(max_length=50,null=False,choices=Stud_or_not)
    def __str__(self):
        return self.FirstName
class UserAccount(AbstractUser):
      Role=models.ForeignKey(Role,on_delete=models.CASCADE,null=True,blank=True)
      username=models.CharField(max_length=200,null=True,unique=True)
      password=models.CharField(max_length=500)
      User=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
class ArchieveAccount(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=500)
class Settings(models.Model):
    company_name=models.CharField(max_length=500)
    Abrevation_name=models.CharField(max_length=100)
    background_image=models.ImageField(upload_to='images/')
    logo=models.ImageField(upload_to='images/')
    slogan=models.CharField(max_length=600)
    descrption1=models.TextField(max_length=1000)
    slogan1=models.CharField(max_length=600)
    descrption2=models.TextField(max_length=1000)
    slogan2=models.CharField(max_length=600)
    descrption3=models.TextField(max_length=1000)
    streat=models.CharField(max_length=100)
    phone=models.IntegerField()
    email=models.EmailField(max_length=100)
    location=models.CharField(max_length=20)

##################LOG#########
class ActivityLog(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    status_code = models.IntegerField()
class Attendance(models.Model):
    User_id=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    
class FingerPrint(models.Model):
    User_id=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    finger_print=models.BinaryField(null=True,blank=True)

class ChatMessage(models.Model):
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='csender')
    reciever = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='creciever')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
