from django.db import models
from account.models import UserAccount
from django.utils import timezone
from django.conf import settings
from StudentDean.models import Block,Dorm
# Create your models here.
Category=[
    ('Key','Key'),
    ('Locker','Locker'),
    ('Desk','Desk'),
    ('Chair','Chair'),
    ('Bed','Bed'),
    ('Mattress','Mattress'),
    ('Pillow','Pillow'),
    
]
class Properties(models.Model):
    Property_id=models.CharField(max_length=100,unique=True)
    Propery_name=models.CharField(max_length=100)
    property_category=models.CharField(max_length=150 , choices=Category)
    block=models.ForeignKey(Block,on_delete=models.CASCADE)
    room=models.ForeignKey(Dorm,on_delete=models.CASCADE)

class Material(models.Model):
    student=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='student')
    proctor=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='proctor')
    property=models.ForeignKey(Properties,on_delete=models.CASCADE,related_name='property')
    def __str__(self):
        return self.student

class Borrow_Request(models.Model):
    student=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='sender')
    property=models.ForeignKey(Properties,on_delete=models.CASCADE,related_name='property1')
    def __str__(self):
        return self.student

class Exit_Permission(models.Model):
    student=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='student1')
    proctor=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='proctor1')
    materials=models.CharField(max_length=1000)
    date=models.DateField()
class Exit_Permission_Requst(models.Model):
    student=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='sender1')  
    materials=models.CharField(max_length=1000)
    date=models.DateField()
class ReportProblem(models.Model):
    student=models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    problem=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    is_solve=models.CharField(max_length=50, default='Un-Approved')

# if 'username' in request.session:
#         student=User.objects.get(id=pk)
#         student_acc=UserAccount.objects.get(User_id=student.id)
#         username = request.session['username']
#         idd=UserAccount.objects.get(username=username)
#         key=idd.id
#         if ProctorSchedule.objects.filter(user_id=key).exists():
#             materials=Borrow_Request.objects.filter(student_id=student_acc.id)
#             for i in materials:
#                 obj1=Material(student_id=student_acc.id,proctor_id=key,property_id=i.property_id)
#                 obj2=Borrow_Request.objects.get(property_id=i.property_id)
#                 obj1.save()
#                 obj2.delete()
#             messages.info(request,'Succesfully Confirmed!')
#         else:
#             messages.info(request,'You are not Assigned to any Dorm yet!')
#     else:
#         return redirect('login_view')


#################Exit Permission#############
# class Exit_Permision(models.Model):
#     proctor=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='sender')
#     student=models.ForeignKey(UserAccount,on_delete=models.CASCADE,related_name='reciever')
#     date=models.DateField(auto_now=True)


    # def accept(self):
    #     """
    #     Accept a friend request.
    #     Update both SENDER and RECEIVER friend lists.
    #     """
    #     receiver_list = Material.objects.get(student=self.student)
    #     if receiver_list:
    #         receiver_list.add_friend(self.sender)
    #         sender_friend_list = Material.objects.get(student=self.proctor)
    #         if sender_friend_list:
    #             sender_friend_list.add_friend(self.student)
    #             self.is_active = False
    #             self.save()

    # def decline(self):
    #     """
    #     Decline a friend request.
    #     Is it "declined" by setting the `is_active` field to False
    #     """
    #     self.is_active = False
    #     self.save()


    # def cancel(self):
    #     """
    #     Cancel a friend request.
    #     Is it "cancelled" by setting the `is_active` field to False.
    #     This is only different with respect to "declining" through the notification that is generated.
    #     """
    #     self.is_active = False
    #     self.save()




