import datetime
from django.contrib.auth import authenticate,logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_control
from StudentDean.models import AnnouncementStatus, Placement,Block,Dorm,Announcement
from account.models import UserAccount,User,Settings
from django.contrib import messages
from Proctor.models import Borrow_Request,Material,Properties,Exit_Permission_Requst,Exit_Permission
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordChangeView,PasswordChangeForm
from .forms import PasswordChangingForm
from datetime import datetime,date
from Proctor.models import ReportProblem
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def home(request): 
    if 'username' in request.session:
        company=Settings.objects.all()
        for i in company:
            name=i.Abrevation_name
            email=i.email
            phone=i.phone
            location=i.location 
            slogan=i.slogan
            slogan1=i.slogan1
            slogan2=i.slogan2
            descrption1=i.descrption1
            descrption2=i.descrption2
            descrption3=i.descrption3
        a=AnnouncementStatus.objects.filter(user=request.user,is_read=False).count()
        if a==0:
          count=''
        else:
          count=str(a)
        context={"Abrevation_name":name,"email":email,"phone":phone,
                 "location":location,"slogan":slogan,'slogan1':slogan1,
                 "slogan2":slogan2,"descrption1":descrption1,"descrption2":descrption2,
                 "descrption3":descrption3,'count':count}
    else:
        return redirect('login_view')
    return render(request,'Student/index.html',context)

@login_required(login_url='login_view')
def request_material(request):
    if 'username' in request.session:
        username = request.session['username']
        acc=UserAccount.objects.get(username=username)
        user1=acc.id
        user=User.objects.get(id=acc.User_id)
        result=""
        if Borrow_Request.objects.filter(student_id=user1).exists():
            messages.info(request,'You Already Sent request for Materials')
            return redirect('student')
        elif Material .objects.filter(student_id=user1).exists():
            messages.info(request,'You Already Get Materials. You can View your Materials')
            return redirect('student')
        else:
            if Placement.objects.filter(Stud_id_id=user.id).exists():
                plc=Placement.objects.get(Stud_id_id=user.id)
                dorm_id=plc.Room_id
                block_id=plc.Block_id
                Bed=[]
                Key=[]
                Locker=[]
                Desk=[]
                Chair=[]
                Mattress=[]
                Pillow=[]
                if Properties.objects.filter(block_id=block_id,room_id=dorm_id).exists:
                    properties=Properties.objects.filter(block_id=block_id,room_id=dorm_id)
                    for i in properties:
                        if Borrow_Request.objects.filter(property=i.id).exists() or Material.objects.filter(property=i.id).exists():
                            if i.property_category=='Desk':
                                Desk.append(i)
                            elif i.property_category=='Chair':
                                Chair.append(i)
                            
                        else:
                            if i.property_category=='Bed':
                                Bed.append(i)
                            elif i.property_category=='Key':
                                Key.append(i)
                            elif i.property_category=='Locker':
                                Locker.append(i)
                            elif i.property_category=='Mattress':
                                Mattress.append(i)
                            elif i.property_category=='Pillow':
                                Pillow.append(i)
                            elif i.property_category=='Desk':
                                Desk.append(i)
                            elif i.property_category=='Chair':
                                Chair.append(i)
                    contex={'properties':properties,'bed':Bed,'key':Key,'locker':Locker,'mattress':Mattress,'pillow':Pillow,'desk':Desk,'chair':Chair}
                    if request.method=='POST':
                        # print(user1)
                        list=[]
                        if len(Bed) !=0:
                            bed=request.POST['bed']
                            if bed =="":
                                list.append('none')
                            else:
                                list.append(bed)
                        else:
                            list.append('none')
                        if len(Key) !=0:
                            key=request.POST['key']
                            if key=="":
                                list.append('none')
                            else:
                                list.append(key)
                        else:
                            list.append("none")
                        if len(Locker) !=0:
                            locker=request.POST['locker']
                            if locker=="":
                                list.append("none")
                            else:
                                list.append(locker)
                        else:
                            list.append("none")
                        if len(Mattress) !=0:
                            mattress1=request.POST['mattress']
                            if mattress1=="":
                                list.append("none")
                            else:
                                list.append(mattress1)
                        else:
                            list.append('none')
                        if len(Pillow) !=0:
                            pillow1=request.POST['pillow']
                            if pillow1=="":
                                list.append("none")
                            else:
                                list.append(pillow1)
                        else:
                            list.append("none")
                        if Borrow_Request.objects.filter(student=user1).exists():
                            messages.info(request,"You Already requested wait For Approval")
                            pass
                        else:
                            for i in Chair:
                                obj=Borrow_Request(student_id=user1,property_id=i.id)
                                obj.save()
                                print("saved")
                            for i in Desk:
                                obj=Borrow_Request(student_id=user1,property_id=i.id)
                                obj.save()
                                print("saved")
                            for i in list:
                                if i =="none":
                                    pass
                                else:
                                    obj=Borrow_Request(student_id=user1,property_id=i)
                                    obj.save()
                                    print("saved")
                            return  redirect('student')
                return render(request,'Student/borrow_material.html',contex)
            else:
                messages.info(request,'You Donot have Dorm')
                # return redirect('requests')
        
    else:
        return redirect('login_view')
    return render(request,'Student/borrow_material.html')


@login_required(login_url='login_view')
def my_Materials(request):
    if 'username' in request.session:
        username = request.session['username']
        acc=UserAccount.objects.get(username=username)
        if Material.objects.filter(student_id=acc.id).exists():
            material=Material.objects.filter(student_id=acc.id)
            property=[]
            for i in material:
                pprt=Properties.objects.get(id=i.property_id)
                property.append(pprt)
            return render(request,'Student/my_material.html',{'result':property})
        # else:
        #     if Borrow_Request.objects.filter(student_id=acc.id).exists():
        #         messages.info(request,"Your Request in Pending Contact Your Procotor")
        #     else:
        #        messages.info(request,"Your are Requested for Materials.") 
    else:
        return redirect('login_view')
    return render(request,'Student/my_material.html')
@login_required(login_url='login_view')
def decline_request(request,pk):
    if 'username' in request.session:
        if Borrow_Request.objects.filter(id=pk).exists():
            obj=Borrow_Request.objects.get(id=pk) 
            obj.delete()
            return redirect('requests')
    else:
        return redirect('login_view')
    return render(request,'Student/borrow_material.html')



@login_required(login_url='login_view')
def exit_permission(request):
    if 'username' in request.session:
        username = request.session['username']
        acc=UserAccount.objects.get(username=username)
        user1=acc.User_id
        user=User.objects.get(id=user1)
        if Placement.objects.filter(Stud_id_id=user.id):
            if request.method=='POST':
                # materials=request.POST['textss']
                materials= request.POST.get('textss')
                
                today=date.today()
                if Exit_Permission_Requst.objects.filter(student_id=acc.id,date=today).exists():
                    messages.error(request,"No chance to ask for Exit permission today")
                else:
                    obj=Exit_Permission_Requst(student_id=acc.id,materials=materials,date=today)
                    obj.save()
                    messages.info(request,"You Sent Request Succesfully.")
        else:
            messages.info(request,"You Don't Have Dorm You can't do this!.")
                    

    else:
       return redirect('login_view')
    return render(request,'Student/exit_permission.html')
def exit_permission_response(request):
    if 'username' in request.session:
        username = request.session['username']
        acc=UserAccount.objects.get(username=username)
        user1=acc.id
        today=date.today()
        materials=""
        context={}
        if Exit_Permission.objects.filter(date=today,student_id=user1).exists():
            print("gate")
            mt=Exit_Permission.objects.get(date=today,student_id=user1)
            print(mt.materials)
            materials=mt.materials
            st=UserAccount.objects.get(id=mt.student_id)
            usr=User.objects.get(id=st.User_id)
            name=usr.FirstName
            lname=usr.LastName
            full_name=name+" "+lname
            context={'material':materials,'name':full_name}
    else:
       return redirect('login_view')
    return render(request,'Student/viewexitrequestresponse.html',context)
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def viewdorm(request):
    if 'username' in request.session:
        username = request.session['username']
        acc=UserAccount.objects.get(username=username)
        user1=acc.User_id
        user=User.objects.get(id=user1)
        userid=user.Id_no
        if Placement.objects.filter(Stud_id_id=user.id).exists():
            plc=Placement.objects.get(Stud_id_id=user.id)
            dorm_id=plc.Room_id
            block_id=plc.Block_id
            dorm=Dorm.objects.get(id=dorm_id)
            block=Block.objects.get(id=block_id)
            dorm1={'Block':block.Block_name ,'Dorm':dorm.Dorm_name,'Firstname':user.FirstName,'Lastname':user.LastName}
            return render(request,'Student/viewdorm.html',dorm1)
        else:    
            messages.error(request,"You are Not Assigned Dorm Yet")
    else:
       return redirect('login_view')

    return render(request,'Student/viewdorm.html')
@login_required(login_url='login_view')
def view_announce1(request,pk):
    if 'username' in request.session:
        result=Announcement.objects.filter(id=pk)
        #result=Dorm.objects.order_by('Block')
        username = request.session['username']
        us=UserAccount.objects.get(username=username)
        if AnnouncementStatus.objects.filter(user=us.id, announcement=result.first(), is_read=False).exists():
            read = AnnouncementStatus.objects.get(user=us.id, announcement=result.first(), is_read=False)
            read.is_read = True
            read.save()
    else:
        return redirect('login_view')
    return render(request ,'Student/view_announce.html',{"announce":result})

@login_required(login_url='login_view')
def view_announcement(request): 

    if 'username' in request.session:
        username = request.session['username']
        context = {}
        a = UserAccount.objects.get(username=username)
        b1 = Announcement.objects.filter(End_Date__gte=date.today()).order_by('-Active_Date')
        count = []
        for announcement in b1:
            announcement_status = AnnouncementStatus.objects.filter(user=request.user, announcement=announcement).first()
            if announcement_status and not announcement_status.is_read:
                count.append(1)
            else:
                count.append('')
        lst = [{'announcement': announcement, 'count': cnt} for announcement, cnt in zip(b1, count)]
        context = {'announcement_list': lst}
 
    else:
        return redirect('login_view')
    return render(request,'Student/view_announcement.html',context)



def reportProblem(request):
 if 'username' in request.session:
    username=request.session['username']
    acc=UserAccount.objects.get(username=username)
    all=ReportProblem.objects.filter(student=acc)
    context={'problem':all}
    if request.method=='POST':
        text=request.POST['text']
        username = request.session['username']
        acc=UserAccount.objects.get(username=username)
        user1=acc.User_id
        user=User.objects.get(id=user1)
        if Placement.objects.filter(Stud_id=user.id).exists():
          
          problem=ReportProblem.objects.create(student=acc,problem=text,date=date.today())
          problem.save()
          messages.success(request,'Report Successfully...')
        else:
            messages.error(request,'Now you have not a Dorm...')
 return render(request,'Student/report_problem.html',context)


def approve_problem(request,pk):
    if 'username' in request.session:  
        update=ReportProblem.objects.get(id=pk)
        update.is_solve='Approved'
        update.save()
        return redirect('reportProblem')
class PasswordsChangeView(PasswordChangeView):
    from_class=PasswordChangeForm
    # from_class=PasswordChangingForm
    success_url=reverse_lazy('logout')
# @login_required(login_url='login_view')
# def change_paassword(request):

#     if request.method == 'POST':
#         current_pass=request.POST['current_password']
#         password1=request.POST['password1']
#         password2=request.POST['password2']
#         old=make_password(current_pass)
#         print(old)
#         if UserAccount.objects.filter(password=old).exists():
#             if password1==password2:
#                 username = request.session['username']
#                 obj=UserAccount.objects.get(username=username)
#                 new=make_password(password1)
#                 obj.password=new
#                 messages.info(request,"Password Changed Succesfully.")
#                 return redirect('logout')
#             else:
#                 messages.info(request,"Password Doesn't Match!")
#                 return redirect('Std_change_paassword')
#         else:
#             messages.info(request,"Incorrect Old Password Please Correct Your Password")
#             return redirect('Std_change_paassword')
#     return render(request,'Student/change_password.html')



def logout_View(request):
    logout(request)
    #del request.session['username']
    return redirect('index')