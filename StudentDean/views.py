from datetime import datetime,time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from account.models import User,UserAccount,Role
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib import messages
from .serializers import BlockSerializer,DormSerializer,PlacementSerializer,UserSerializer,SaveFileSerializer,UserUploadSerializer
from rest_framework.renderers import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from account.forms import AddAccountForm
from account.models import Settings,ChatMessage
from Proctor.models import Material
import csv,openpyxl, pandas as pd
import os
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
def settings():
    company=Settings.objects.all()
    for i in company:
        name=i.Abrevation_name
        context1={'Abrevation_name':name}
    return context1
# Create your views here.
@login_required(login_url='login_view')
def announce(request):
    if 'username' in request.session:
        # # form=AnnouncementForm(request.POST or None) 
        if request.method=='POST':
            Title=request.POST['Title']
            Image=''
            Content=''
            try:
                Content=request.POST['Content']
                Image=request.FILES['Image']
                # uploaded_file_url = fs.url(filename)
                

            except:
                pass
            
           
            # fs = FileSystemStorage()
            # filename = fs.save(Image.name, Image)
            
           

            if Content=='' and Image=='':
             messages.error(request,'One of (Content or File) Must be Required.')
            else:
                
                Active_Date=datetime.now()
                End_Date=request.POST['End_Date']
               
                end=datetime.strptime(End_Date, '%Y-%m-%d')
               
               
                if end<Active_Date:
                    messages.error(request,'Enter Correct End date.')
                else:
                    annou=Announcement.objects.create(Title=Title,Content=Content,File=Image,Active_Date=Active_Date,End_Date=End_Date)
                    annou.save()
                    aa=Role.objects.get(R_name='Student')
                    stu=UserAccount.objects.filter(Role=aa)
                    for i in stu:
                        if AnnouncementStatus.objects.filter(user=i,announcement=annou,is_read=False).exists():
                            pass
                        else:
                            a1=AnnouncementStatus.objects.create(user=i,announcement=annou,is_read=False)
                            a1.save()
                    messages.success(request,'Announce Successfully.')
        context={'date':datetime.now()}
        setting=settings()
        context={**context,**setting}
        pass
    else:
        return redirect('login_view')

    return render(request,'StudentDean/announce.html',context)
# Create your views here.
@login_required(login_url='login_view')
def manage_announce(request):
    if 'username' in request.session:
       
        announce=Announcement.objects.filter(End_Date__gte=datetime.now()).order_by('-Active_Date')
        # for i in announce:
        #     i.Image='http://127.0.0.1:8000/media/'+str(i.Image)
        context={'announce':announce}
        setting=settings()
        context={**context,**setting}
    else:
        return redirect('login_view')
    return render(request,'StudentDean/manage_announcement.html',context)

@login_required(login_url='login_view')
def view_announce(request,pk):
    if 'username' in request.session:
        result=Announcement.objects.filter(id=pk)
        #result=Dorm.objects.order_by('Block')
    else:
        return redirect('login_view')
    return render(request ,'StudentDean/view_announce.html',{"announce":result})
@login_required(login_url='login_view')
def Edit_Announcement(request,pk):
    if 'username' in request.session:
        result=Announcement.objects.get(id=pk)
        result1=Announcement.objects.all()
        form=AddAnnouncement(request.POST or None,instance=result)
        context = { 'res': result,'form':form} 
        if form.is_valid():
            form.save()
            messages.success(request,"Data Updated Succesfully!")
            return redirect('manage_announce')
            # return render(request ,'StudentDean/view_announce.html',{"Block":result1})
    else:
        return redirect('login_view')
    return render(request,'StudentDean/Edit_Announcement.html',context)
@login_required(login_url='login_view')
def home(request):
    if 'username' in request.session:
        username = request.session['username']
    else:
        return redirect('login_view')
    setting=settings()
    return render(request, 'Sdeanindex.html',setting)
####################INFO#######################
@login_required(login_url='login_view')
def OverallInfo(request):
    if 'username' in request.session:
        total_Placed=Placement.objects.all().count()
        total_dorms=Dorm.objects.all().count()
        placed_male=0
        placed_female=0
        males_dorm=0
        females_dorm=0
        tota_available_dorm=0
        males_availabe_dorm=0
        females_available_dorm=0
        tota_available_dorm_capacity=0
        males_availabe_dorm_capacity=0
        females_available_dorm_capacity=0
        pl=Placement.objects.all()
        for i in pl:
            acc=UserAccount.objects.get(id=i.Stud_id_id)
            usr=User.objects.get(id=acc.User_id)
            if usr.Gender == 'Male':
                placed_male+=1
            else:
                placed_female+1
        drm=Dorm.objects.all()
        maledormcapacity=0
        femaledormcapacity=0
        for i in drm:
            blk=Block.objects.get(id=i.Block_id)
            if blk.Block_purpose=="Males Block":
                males_dorm+=1
                if i.Status=='Active' and blk.Status=="Active":
                    males_availabe_dorm+=1
                    nn=i.Capacity
                    maledormcapacity+=int(nn)
            else:
                females_dorm+=1
                if i.Status=='Active' and blk.Status=="Active":
                    females_available_dorm+=1
                    nn=i.Capacity
                    femaledormcapacity+=int(nn)
        tota_available_dorm=males_availabe_dorm+females_available_dorm
        males_availabe_dorm_capacity=maledormcapacity-placed_male
        females_available_dorm_capacity=femaledormcapacity-placed_female
        tota_available_dorm_capacity=males_availabe_dorm_capacity+females_available_dorm_capacity
        
        context={'total_Placed':total_Placed,'total_dorms':total_dorms,'placed_male':placed_male,
                 'placed_female':placed_female,'males_dorm':males_dorm,'females_dorm':females_dorm,
                 "tota_available_dorm":tota_available_dorm,'males_availabe_dorm':males_availabe_dorm,
                 'females_available_dorm':females_available_dorm,'tota_available_dorm_capacity':tota_available_dorm_capacity,
                 'males_availabe_dorm_capacity':males_availabe_dorm_capacity,
                 "females_available_dorm_capacity":females_available_dorm_capacity}
    else:
        return redirect('login_view')
    return render(request,"StudentDean/dormitory_information.html",context)
################USER MANAGEMENT################
def addEmployee(request):
    if 'username' in request.session:
        form=EmployeeForm(request.POST or None)
        if request.method=='POST':
            if form.is_valid():
                Id_no=request.POST['Id_no']
                if User.objects.filter(Id_no=Id_no).exists():
                    messages.info(request,'This User is Already Registered!...')
                    return redirect('addemployee')
                else:
                    form.save()
                    messages.info(request,'User Added Succesfully!...')
                    return redirect('addemployee')
            else:
                messages.info(request,'Invalid Form!...')
    else:
        return redirect('login_view')
    context={'form':form}
    setting=settings()
    context={**context,**setting} 
    return render(request,'StudentDean/Employee_Register.html',context)
@login_required(login_url='login_view')
def Import_User(request):
    if 'username' in request.session:
        block_type=BlockType.objects.all()
        count=0
        try:
            if request.method == 'POST' and request.FILES['myfile']: 
                blocktype=request.POST['block_type']
                block_type_id=BlockType.objects.get(Block_Type=blocktype)
                myfile = request.FILES['myfile']             
                empexceldata = pd.read_excel(myfile)        
                dbframe = empexceldata
                
                for dbframe in dbframe.itertuples():
                
                    if User.objects.filter(Id_no=dbframe.Id_no).exists():          
                        continue
                    else:
                        
                        obj = User.objects.create(Id_no=dbframe.Id_no,FirstName=dbframe.FirstName,LastName=dbframe.LastName,
                                                Gender=dbframe.Gender,phone_no=dbframe.phone_no,
                                                stream=dbframe.stream,collage=dbframe.collage,
                                                Department=dbframe.Department, 
                                                Year_of_Student=dbframe.Year_of_Student,
                                                Campus=block_type_id,
                                                Disability=dbframe.Disability,
                                                Emergency_responder_name=dbframe.Emergency_responder_name,
                                                Emergency_responder_address=dbframe.Emergency_responder_address, 
                                                Emergency_responder_phone_no=dbframe.Emergency_responder_phone_no)
                        obj.save()
                        count+=1 
                if count==0:
                    messages.warning(request,"All User's are Already Registered...!")
                elif count==1:
                    messages.success(request,"One User is Registered Succesfully...!")
                else:
                    mess=str(count)+" Users  added successfuly...!!"
                    messages.success(request,mess)
                    # return render(request, 'StudentDean/uploadusers.html', {'uploaded_file_url': uploaded_file_url}) 
                #
        except:
            msg= 'Error Occured after Inserting '+str(count) +' Data Please Correct Your the table'
            messages.error(request,msg)
    else:
        return redirect('login_view')   
    context={'block_type':block_type}
    setting=settings()
    context={**context,**setting} 
    return render(request, 'StudentDean/uploadusers.html',context)

@login_required(login_url='login_view')
def grantrole(request):
    if 'username' in request.session:
        role1=Role.objects.get(R_name="Proctor")
        role2=Role.objects.get(R_name="Employee")
        role3=Role.objects.get(R_name="Supervisor")
        result=UserAccount.objects.filter(Role_id=role2)| UserAccount.objects.filter(Role_id=role1)| UserAccount.objects.filter(Role_id=role3)
        #result2=UserAccount.objects.filter(Role_id=4)
        # for i in result:
        #     print(i.username)
        if request.method=="POST":
            searched=request.POST["searched"]
            if UserAccount.objects.filter(username=searched): 
                usacc=UserAccount.objects.filter(username=searched)
                context={'Result':usacc}
                setting=settings()
                context={**context,**setting}
                return render(request,'StudentDean/grantrole.html',context)
    else:
        return redirect('login_view')
    context={'Result':result}
    setting=settings()
    context={**context,**setting} 
    return render(request,'StudentDean/grantrole.html',context)
@login_required(login_url='login_view')
def updaterole(request,pk):
    if 'username' in request.session:
        result=UserAccount.objects.get(id=pk)
        if request.method=='POST':
            role=request.POST['role']
            print(role)
            nn=Role.objects.get(R_name=role)
            result.Role_id=nn.id
            result.save()
            messages.success(request, "Role Updated Succesfully...")
    else:
        return redirect('login_view')
    context={"Result":result}
    setting=settings()
    context={**context,**setting} 
    return render(request,'StudentDean/updaterole.html',context)
@login_required(login_url='login_view')
def update_employee(request,pk):
    if 'username' in request.session:
        # EmployeeForm   
        entry=User.objects.get(id=pk)
        if request.method == 'POST':
            form = EmployeeForm(request.POST, instance=entry)
            if form.is_valid():
                form.save()
                messages.success(request,'Information Edited Succesfully!')
            # Redirect to a success page or return a response
                return redirect('view_employee')
        else:
            form = EmployeeForm(instance=entry)
        context={'form': form}
        setting=settings()
        context={**context,**setting}
    else:
        return redirect('login_view') 
    return render(request,'StudentDean/updateEmployee.html',context)
@login_required(login_url='login_view')
def delete_employee(request,pk):
    usr=User.objects.get(id=pk)
    usr.delete()
    messages.error(request,'Employee Deleted Succesfully!')
    return redirect('view_employee')
@login_required(login_url='login_view')
def view_employee(request):
    if 'username' in request.session:
        role1=Role.objects.get(R_name="Supervisor")
        role2=Role.objects.get(R_name="Proctor")
        result1=UserAccount.objects.filter(Role_id=role1.id)
        result2=UserAccount.objects.filter(Role_id=role2.id)
        user=[]
        role=[]
        for i in  result1:
            usr=User.objects.get(id=i.User_id)
            user.append(usr)
            r=Role.objects.get(id=i.Role_id)
            role.append(r.R_name)
        for i in  result2:
            usr=User.objects.get(id=i.User_id)
            user.append(usr)
            r=Role.objects.get(id=i.Role_id)
            role.append(r.R_name)
        lst=[{'item1':t[0],'item2':t[1]} for t in zip(user,role)] 
        context={'result':lst}
        setting=settings()
        context={**context,**setting}
    else:
        return redirect('login_view')
    return render(request,"StudentDean/View_employee.html",context)
@login_required(login_url='login_view')
def account_activate_deactivate(request):
    if request.method=='POST':
        id=request.POST['user_id']
        acc=UserAccount.objects.get(id=id)
        if acc.is_active:
            acc.is_active=False
        else:
            acc.is_active=True
        acc.save()
    return redirect('S_grantrole')
#################DORMITORY###############
@login_required(login_url='login_view')
def blockType(request):
    if 'username' in request.session:
        form=BlockTypeForm(request.POST or None)
        if request.method=='POST':
            if form.is_valid():
                block=request.POST['Block_Type']
                if BlockType.objects.filter(Block_Type=block).exists() :
                    messages.error(request, "This Block Type is already Registerd")
                    return redirect('addblocktype')
                else:
                    form.save()
                    messages.success(request,"Block Type Registered Succesfully")
                    return redirect('addblocktype')
    else:
        return redirect('login_view')
    context={'form':form}
    setting=settings()
    context={**context,**setting} 
    return render(request,'StudentDean/add_block_type.html',context)
@login_required(login_url='login_view')
def BlockAdd(request):
    if 'username' in request.session:
        form=AddBlockForm1(request.POST or None)
        if request.method=='POST':
            if form.is_valid():
                block=request.POST['Block_name']
                if Block.objects.filter(Block_name=block).exists() :
                    messages.error(request, "This Block is already Registerd")
                    return redirect('blockadd')
                else:
                    form.save()
                    messages.success(request,"Block Registered Succesfully")
                    return redirect('blockadd')
    else:
        return redirect('login_view')
    context={'form':form}
    setting=settings()
    context={**context,**setting}
    return render(request,'StudentDean/addblock.html',context)
@login_required(login_url='login_view')
def add_dorm(request):
    if 'username' in request.session:
        form=AddDorm(request.POST or None)
        if request.method=='POST':
            if form.is_valid():
                block=request.POST['Block']
                dorm=request.POST['Dorm_name']
                count_dorm=Dorm.objects.filter(Block_id=block).count()
                block1=Block.objects.get(id=int(block))
                block_capacity=block1.Block_Capacity
                if count_dorm<block_capacity:
                    if Dorm.objects.filter(Dorm_name=dorm,Block=block).exists() :
                        messages.error(request, "This Dorm is already Registerd")
                        return redirect('add_dorm')
                    else:
                        form.save()
                        messages.success(request,"Dorm Registered Succesfully")
                        return redirect('add_dorm')
                else:
                    messages.info(request,"This Block Full You Can't Add Dorm")
                    return redirect('add_dorm') 
    else:
        return redirect('login_view')
    context={'form':form}
    setting=settings()
    context={**context,**setting}
    return render(request,'StudentDean/add_dorm.html',context)
@login_required(login_url='login_view')
def viewblock(request):
    if 'username' in request.session:
        result=Block.objects.order_by('Block_name')
    else:
        return redirect('login_view')
    context={"Block":result}
    setting=settings()
    context={**context,**setting}
    return render(request ,'StudentDean/viewblock.html',context)
@login_required(login_url='login_view')
def viewdorm(request,pk):
    if 'username' in request.session:
        result=Dorm.objects.filter(Block=pk)
        #result=Dorm.objects.order_by('Block')
    else:
        return redirect('login_view')
    context={"Dorm":result }
    setting=settings()
    context={**context,**setting}
    return render(request ,'StudentDean/viewdorm.html',context)
@login_required(login_url='login_view')
def updateblock(request,pk):
    if 'username' in request.session:
        result=Block.objects.get(id=pk)
        result1=Block.objects.all()
        form=AddBlockForm(request.POST or None,instance=result)
        context = { 'res': result,'form':form} 
        setting=settings()
        context={**context,**setting}
        if form.is_valid():
            form.save()
            messages.success(request,"Data Updated Succesfully!")
            context={"Block":result1}
            setting=settings()
            context={**context,**setting}
            return render(request ,'StudentDean/viewblock.html',context)
    else:
        return redirect('login_view')
    
    return render(request,'StudentDean/updateblock.html',context)
@login_required(login_url='login_view')
def updatedorm(request,pk):
    if 'username' in request.session:
        result=Dorm.objects.get(id=pk)
        result1=Dorm.objects.order_by('Block')
        form=AddDorm(request.POST or None,instance=result)
        context = { 'res': result,'form':form} 
        setting=settings()
        context={**context,**setting}
        if form.is_valid():
            form.save()
            messages.success(request,"Data Updated Succesfully!")
            context={"Dorm":result1}
            setting=settings()
            context={**context,**setting}
            return render(request ,'StudentDean/viewdorm.html',context)
    else:
        return redirect('login_view')
    return render(request,'StudentDean/updatedorm.html',context)
@login_required(login_url='login_view')
def delatedorm(request,pk):
    if 'username' in request.session:
        result=Dorm.objects.get(id=pk)
        result1=Dorm.objects.order_by('Block')
        result.delete() 
        messages.error(request,"Data Deleted Succesfully!")
    else:
        return redirect('login_view')
    
    
    return redirect('viewblock')
@login_required(login_url='login_view')
def delateblock(request,pk):
    if 'username' in request.session:
        result=Block.objects.get(id=pk)
        result1=Block.objects.order_by('Block_name')
        result.delete() 
        messages.error(request,"Data Deleted Succesfully!") 
    else:
        return redirect('login_view')
    return redirect('viewblock')

############PLACEMENT######################
@login_required(login_url='login_view')
def PlaceStudent(request):
    count=0
    student = User.objects.filter(stream__in=['natural', 'social'])
    blk=Block.objects.all()
    Id=[]
    AllStudent=[]
    for i in student:
        if Placement.objects.filter(Stud_id_id=i.id).exists():
            pass
        else:
            AllStudent.append(i)
    context = {"AllStudent":AllStudent,'Block':blk} 
    setting=settings()
    context={**context,**setting}
    ###################################
    if request.method=="POST":
        criteria=request.POST.getlist('criteria')
        StudentId=request.POST.getlist('users')
        searched=request.POST['searchedd']
        if searched =="":
            pass
        else:
            student = User.objects.filter(stream__in=['natural', 'social'])
            blk=Block.objects.all()
            Id=[]
            AllStudent=[]
            for i in student:
                result=User.objects.get(id=i.id)
                if result.collage == searched or result.Department == searched or result.Year_of_Student==searched or result.Disability==searched:
                    if Placement.objects.filter(Stud_id_id=result.id).exists():
                        pass
                    else:
                        AllStudent.append(result)
            context = {"AllStudent":AllStudent,'Block':blk}
            setting=settings()
            context={**context,**setting}
            return render(request,'StudentDean/Placestudent.html',context)
        social_male_student=[]
        social_male_student_disable=[]
        social_female_student=[]
        social_female_student_disable=[]
        natural_male_student=[]
        natural_male_student_disable=[]
        natural_female_student=[]
        natural_female_student_disable=[]
        for data in StudentId:
            student=User.objects.get(Id_no=data)
            b=[]
            a1=data
            a2=student.FirstName
            a3=student.LastName
            a4=student.Gender
            a5=student.Department
            a6=student.collage
            a7=student.stream
            a8=student.Year_of_Student
            a9=student.Disability
            a10=student.Campus

            b.append(a1)
            b.append(a2)
            b.append(a3)
            b.append(a4)
            b.append(a5)
            b.append(a6)
            b.append(a7)
            b.append(a8)
            b.append(a9)
            b.append(a10)       
            
            
            if b[3]=="Male" or b[3]=='M':
                if a9 =='Disable':
                    if a7=="social":
                        social_male_student_disable.append(b)
                    elif a7=='natural':
                        natural_male_student_disable.append(b)
                else:
                    if a7=="social":
                        social_male_student.append(b)
                    elif a7=='natural':
                        
                        natural_male_student.append(b)
            else:
                if b[8]=='Disable':
                    if a7=="social":
                        social_female_student_disable.append(b)
                    elif a7=='natural':
                        natural_female_student_disable.append(b)
                else:
                    if a7=="social":
                        social_female_student.append(b)
                    elif a7=='natural':
                        natural_female_student.append(b)
        sorted_social_male_student_disable=sorted(social_male_student_disable,key=lambda x:(x[1],x[2]))
        sorted_natural_male_student_disable=sorted(natural_male_student_disable,key=lambda x:(x[1],x[2]))
        sorted_natural_female_student_disable=sorted(natural_female_student_disable,key=lambda x:(x[1],x[2]))
        sorted_social_female_student_disable=sorted(social_female_student_disable,key=lambda x:(x[1],x[2]))
        if 'collage' in criteria:
            if 'department' in criteria:
                if 'batch' in criteria:
                    sorted_male_social_student=sorted(social_male_student,key=lambda x:(x[5],x[4],x[7]))
                    sorted_female_social_student=sorted(social_female_student,key=lambda x:(x[5],x[4],x[7]))
                    sorted_male_natural_student=sorted(natural_male_student,key=lambda x:(x[5],x[4],x[7]))
                    sorted_female_natural_student=sorted(natural_female_student,key=lambda x:(x[5],x[4],x[7]))
                else:
                    sorted_male_social_student=sorted(social_male_student,key=lambda x:(x[5],x[4]))
                    sorted_female_social_student=sorted(social_female_student,key=lambda x:(x[5],x[4]))
                    sorted_male_natural_student=sorted(natural_male_student,key=lambda x:(x[5],x[4]))
                    sorted_female_natural_student=sorted(natural_female_student,key=lambda x:(x[5],x[4]))
            else:  
                if 'batch' in criteria:
                    sorted_male_social_student=sorted(social_male_student,key=lambda x:(x[5],x[7]))
                    sorted_female_social_student=sorted(social_female_student,key=lambda x:(x[5],x[7]))
                    sorted_male_natural_student=sorted(natural_male_student,key=lambda x:(x[5],x[7]))
                    sorted_female_natural_student=sorted(natural_female_student,key=lambda x:(x[5],x[7]))
                else:
                    sorted_male_social_student=sorted(social_male_student,key=lambda x:(x[5]))
                    sorted_female_social_student=sorted(social_female_student,key=lambda x:(x[5]))
                    sorted_male_natural_student=sorted(natural_male_student,key=lambda x:(x[5]))
                    sorted_female_natural_student=sorted(natural_female_student,key=lambda x:(x[5]))
        else:
                    
            if 'department' in criteria:
                
                if 'batch' in criteria:
                    
                    sorted_male_social_student=sorted(social_male_student,key=lambda x:(x[4],x[7]))
                    sorted_female_social_student=sorted(social_female_student,key=lambda x:(x[4],x[7]))
                    sorted_male_natural_student=sorted(natural_male_student,key=lambda x:(x[4],x[7]))
                    sorted_female_natural_student=sorted(natural_female_student,key=lambda x:(x[4],x[7]))
                else:
                    
                    sorted_male_social_student=sorted(social_male_student,key=lambda x:(x[4]))
                    sorted_female_social_student=sorted(social_female_student,key=lambda x:(x[4]))
                    sorted_male_natural_student=sorted(natural_male_student,key=lambda x:(x[4]))
                    sorted_female_natural_student=sorted(natural_female_student,key=lambda x:(x[4]))
            else:
                if 'batch' in criteria:
                    sorted_male_social_student=sorted(social_male_student,key=lambda x:(x[7]))
                    sorted_female_social_student=sorted(social_female_student,key=lambda x:(x[7]))
                    sorted_male_natural_student=sorted(natural_male_student,key=lambda x:(x[7]))
                    sorted_female_natural_student=sorted(natural_female_student,key=lambda x:(x[7]))
                    
                else:
                    sorted_male_social_student=social_male_student
                    sorted_female_social_student=social_female_student
                    sorted_male_natural_student=natural_male_student
                    sorted_female_natural_student=natural_female_student

        # print(sorted_male_social_student)
        # print(sorted_female_social_student)
        # print(sorted_male_natural_student)
        # print(sorted_female_natural_student)
        # print(sorted_social_male_student_disable)
        # print(sorted_social_female_student_disable)
        # print(sorted_natural_male_student_disable)
        # print(sorted_natural_female_student_disable)
        #print(sorted_male_natural_student[0]) 
        blkk=request.POST['selected_block']
        if blkk=="":
            order=['Block','Dorm_name']
            dorm=Dorm.objects.all().order_by(*order).values() 
        else:
            order=['Dorm_name']
            block_id=Block.objects.get(Block_name=blkk)
            dorm=Dorm.objects.filter(Block_id=block_id.id).order_by(*order).values()
        
            
        for dorm1 in dorm:
            #print(dorm1['Dorm_name'],dorm1['Capacity']) 
            bl=dorm1['Block_id']
            block=Block.objects.get(id=bl)
            #################place Disable Students#################### 
            if str(block.Block_purpose)=='Males Block'and dorm1['Status']=='Active' and str(block.Status)=='Active':
                for student in sorted_social_male_student_disable:
                
                    if str(student[9]) ==str(block.Block_type):
                        if str(dorm1['Floor'])=='Floor-1':
                            cnt=Placement.objects.filter(Block_id=block.id,Room_id=dorm1['id']).count()
                            
                            if int(cnt)<int(dorm1['Capacity']):
                                user=User.objects.get(Id_no=student[0])
                                # usracc=UserAccount.objects.get(User_id=user.id)
                                if Placement.objects.filter(Stud_id=user.id).exists():
                                 pass
                                else:
                                    usr=User.objects.get(Id_no=student[0])
                                    # userr=UserAccount.objects.get(User_id=usr.id)
                                    room=Dorm.objects.get(Dorm_name=dorm1['Dorm_name'],Block=block.id)
                                    place=Placement(Stud_id=usr,Block=block,Room=room)
                                    place.save()
                                    count=count+1
                            else:
                                break
                    else:
                        pass 
                for student in sorted_natural_male_student_disable:
                    if str(student[9]) ==str(block.Block_type):
                        if str(dorm1['Floor'])=='Floor-1':
                            cnt=Placement.objects.filter(Block_id=block.id,Room_id=dorm1['id']).count()
                            
                            if int(cnt)<int(dorm1['Capacity']):
                                user=User.objects.get(Id_no=student[0])
                                # usracc=UserAccount.objects.get(User_id=user.id)
                                if Placement.objects.filter(Stud_id=user.id).exists():
                                 pass
                                else:
                                    usr=User.objects.get(Id_no=student[0])
                                    # userr=UserAccount.objects.get(User_id=usr.id)
                                    room=Dorm.objects.get(Dorm_name=dorm1['Dorm_name'],Block=block.id)
                                    place=Placement(Stud_id=usr,Block=block,Room=room)
                                    place.save()
                                    count=count+1
                            else:
                                break
                    else:
                        pass
            elif str(block.Block_purpose)=='Females Block'and dorm1['Status']=='Active' and str(block.Status)=='Active':
                for student in sorted_social_female_student_disable:
                    if str(student[9]) ==str(block.Block_type):
                        if str(dorm1['Floor'])=='Floor-1':
                            cnt=Placement.objects.filter(Block_id=block.id,Room_id=dorm1['id']).count()
                            
                            if int(cnt)<int(dorm1['Capacity']):
                                user=User.objects.get(Id_no=student[0])
                                # usracc=UserAccount.objects.get(User_id=user.id)
                                if Placement.objects.filter(Stud_id=user.id).exists():
                                 pass
                                else:
                                    usr=User.objects.get(Id_no=student[0])
                                    # userr=UserAccount.objects.get(User_id=usr.id)
                                    room=Dorm.objects.get(Dorm_name=dorm1['Dorm_name'],Block=block.id)
                                    place=Placement(Stud_id=usr,Block=block,Room=room)
                                    place.save()
                                    count=count+1
                            else:
                                break
                    else:
                        pass 
                for student in sorted_natural_female_student_disable:
                    if str(student[9]) ==str(block.Block_type):
                        if str(dorm1['Floor'])=='Floor-1':
                            cnt=Placement.objects.filter(Block_id=block.id,Room_id=dorm1['id']).count()
                            
                            if int(cnt)<int(dorm1['Capacity']):
                                user=User.objects.get(Id_no=student[0])
                                # usracc=UserAccount.objects.get(User_id=user.id)
                                if Placement.objects.filter(Stud_id=user.id).exists():
                                 pass
                                else:
                                    usr=User.objects.get(Id_no=student[0])
                                    # userr=UserAccount.objects.get(User_id=usr.id)
                                    room=Dorm.objects.get(Dorm_name=dorm1['Dorm_name'],Block=block.id)
                                    place=Placement(Stud_id=usr,Block=block,Room=room)
                                    place.save()
                                    count=count+1
                            else:
                                break
                    else:
                        pass
            
           
            #################place Non Disable Students#################### 
               
            if str(block.Block_purpose)=='Males Block'and dorm1['Status']=='Active' and str(block.Status)=='Active':
                for student in sorted_male_social_student:
                    if str(student[9]) ==str(block.Block_type):
                        if str(dorm1['Floor'])=='Floor-1':
                            cnt=Placement.objects.filter(Block_id=block.id,Room_id=dorm1['id']).count()
                            
                            if int(cnt)<int(dorm1['Capacity']):
                                user=User.objects.get(Id_no=student[0])
                                # usracc=UserAccount.objects.get(User_id=user.id)
                                if Placement.objects.filter(Stud_id=user.id).exists():
                                 pass
                                else:
                                    usr=User.objects.get(Id_no=student[0])
                                    # userr=UserAccount.objects.get(User_id=usr.id)
                                    room=Dorm.objects.get(Dorm_name=dorm1['Dorm_name'],Block=block.id)
                                    place=Placement(Stud_id=usr,Block=block,Room=room)
                                    place.save()
                                    count=count+1
                            else:
                                break
                    else:
                        pass 
                # print(sorted_male_natural_student)
                for student in sorted_male_natural_student:
                
                    if str(student[9]) ==str(block.Block_type):
                        if str(dorm1['Floor'])=='Floor-1':
                            cnt=Placement.objects.filter(Block_id=block.id,Room_id=dorm1['id']).count()
                            
                            if int(cnt)<int(dorm1['Capacity']):
                                user=User.objects.get(Id_no=student[0])
                                # usracc=UserAccount.objects.get(User_id=user.id)
                                if Placement.objects.filter(Stud_id=user.id).exists():
                                 pass
                                else:
                                    usr=User.objects.get(Id_no=student[0])
                                    # userr=UserAccount.objects.get(User_id=usr.id)
                                    room=Dorm.objects.get(Dorm_name=dorm1['Dorm_name'],Block=block.id)
                                    place=Placement(Stud_id=usr,Block=block,Room=room)
                                    place.save()
                                    count=count+1
                            else:
                                break
                    else:
                        pass
            elif str(block.Block_purpose)=='Females Block'and dorm1['Status']=='Active' and str(block.Status)=='Active':
                for student in sorted_female_social_student:
                    
                    if str(student[9]) ==str(block.Block_type):
                        if str(dorm1['Floor'])=='Floor-1':
                            cnt=Placement.objects.filter(Block_id=block.id,Room_id=dorm1['id']).count()
                            
                            if int(cnt)<int(dorm1['Capacity']):
                                user=User.objects.get(Id_no=student[0])
                                # usracc=UserAccount.objects.get(User_id=user.id)
                                if Placement.objects.filter(Stud_id=user.id).exists():
                                 pass
                                else:
                                    usr=User.objects.get(Id_no=student[0])
                                    # userr=UserAccount.objects.get(User_id=usr.id)
                                    room=Dorm.objects.get(Dorm_name=dorm1['Dorm_name'],Block=block.id)
                                    place=Placement(Stud_id=usr,Block=block,Room=room)
                                    place.save()
                                    count=count+1
                            else:
                                break
                    else:
                        pass
                for student in sorted_female_natural_student:
                   
                    if str(student[9]) ==str(block.Block_type):
                        if str(dorm1['Floor'])=='Floor-1':
                            cnt=Placement.objects.filter(Block_id=block.id,Room_id=dorm1['id']).count()
                            
                            if int(cnt)<int(dorm1['Capacity']):
                                user=User.objects.get(Id_no=student[0])
                                # usracc=UserAccount.objects.get(User_id=user.id)
                                if Placement.objects.filter(Stud_id=user.id).exists():
                                 pass
                                else:
                                    usr=User.objects.get(Id_no=student[0])
                                    # userr=UserAccount.objects.get(User_id=usr.id)
                                    room=Dorm.objects.get(Dorm_name=dorm1['Dorm_name'],Block=block.id)
                                    place=Placement(Stud_id=usr,Block=block,Room=room)
                                    place.save()
                                    count=count+1
                            else:
                                break
                    else:
                        pass  
        if count == 0:
            messages.info(request,"No new Students Placed")
        elif count ==1:
            messages.info(request,"Only 1 Stundents Placed")  
        else:
            msg=str(count)+" Stundents Placed Succusfully"
            messages.info(request,msg)   
        return redirect('placestudent')         

    return render(request, 'StudentDean/Placestudent.html',context)

@login_required(login_url='login_view')
def managePlacement(request):
    if 'username' in request.session:
        # result11=Placement.objects.all()
        orderlist=['Block_id','Room_id']
        result=Placement.objects.all().order_by(*orderlist)
        # for i in result:
        #     print(i.Block)
        S_Block=[]
        S_Room=[]
        Stud=[]
        ##########
        Room=[]
        block=[]
        User_acc=[]
        user_id=[]
        count=0
        for i in result:
            block.append(i.Block_id)
            Room.append(i.Room_id)
            usr=User.objects.get(id=i.Stud_id_id)
            Stud.append(usr)
            blk=Block.objects.get(id=block[count])
            S_Block.append(blk.Block_name)
            rm=Dorm.objects.get(id=Room[count])
            S_Room.append(rm.Dorm_name)
            count+=1

        lst=[{'item1':t[0],'item2':t[1],'item3':t[2],'item4':t[3]} for t in zip(Stud,S_Block,S_Room,result)] 
        context={'List':lst}
        setting=settings()
        context={**context,**setting}
        if request.method =='POST':
            searched=request.POST['searched']
            result1=Placement.objects.all()
            result=User.objects.filter(Department__contains=searched)| User.objects.filter(Id_no=searched)
            user_id=[]
            Block_name1=[]
            Dorm_name1=[]
            if result != "":
                for i in result:
                    if Placement.objects.filter(Stud_id_id=i.id):
                        
                        pl=Placement.objects.get(Stud_id_id=i.id)
                        # print(pl)
                        user_id.append(i)
                        blk=Block.objects.get(id=pl.Block_id)
                        drm=Dorm.objects.get(id=pl.Room_id)
                        Dorm_name1.append(drm.Dorm_name)
                        Block_name1.append(blk.Block_name)
                lst=[{'item1':t[0],'item2':t[1],'item3':t[2],'item4':t[3]} for t in zip(user_id,Block_name1,Dorm_name1,result1)] 
                context={'List':lst}
                setting=settings()
                context={**context,**setting}
            if Block.objects.filter(Block_name=searched).exists():
                block=Block.objects.get(Block_name=searched)
                
                if Placement.objects.filter(Block_id=block.id).exists():
                    
                    pl=Placement.objects.filter(Block_id=block.id)
                    for i in pl:  
                        Block_name1.append(block.Block_name)
                        
                        drm1=Dorm.objects.get(id=i.Room_id)
                        Dorm_name1.append(drm1.Dorm_name)
                        usr=User.objects.get(id=i.Stud_id_id)
                        user_id.append(usr)
                lst=[{'item1':t[0],'item2':t[1],'item3':t[2],'item4':t[3]} for t in zip(user_id,Block_name1,Dorm_name1,result1)] 
                context={'List':lst}
                setting=settings()
                context={**context,**setting}
            return render(request, "StudentDean/viewPlacementInfo.html",context)
    else:
        return redirect('login_view')
    return render(request,"StudentDean/viewPlacementInfo.html",context)
@login_required(login_url='login_view')
def updateStudent(request,pk):
    if 'username' in request.session:
        result=Placement.objects.get(id=pk)
        # user_acc=UserAccount.objects.get(id=result.Stud_id_id)
        user=User.objects.get(id=result.Stud_id_id)
        Stud_id=str(user.Id_no)
        bl=Block.objects.get(id=result.Block_id)
        print(bl.id)
        dormss=Dorm.objects.filter(Block_id=bl.id)
        #result1=Placement.objects.order_by(*orderlist)
        # form1=AddPlacementForm(request.POST or None,instance=result)
        Bname=str(bl.Block_name)
        context = { 'res': dormss,  'blockk': Bname, 'Student':Stud_id }
        setting=settings()
        context={**context,**setting}
        if request.method =='POST':
            block=request.POST['block']
            room=request.POST['room']
            
            blockk=Block.objects.get(Block_name=block)
            if Dorm.objects.filter(Block_id=blockk.id ,Dorm_name=room).exists():
                roomm=Dorm.objects.get(Block_id=blockk.id ,Dorm_name=room)
                rs=Placement.objects.filter(Block_id=blockk.id,Room_id=roomm.id).count()
                print(roomm.Capacity)
                print(rs)
                if int(roomm.Capacity) > int(rs):
                    result=Placement.objects.get(id=pk)
                    result.Block=blockk
                    result.Room=roomm
                    result.save()
                    messages.success(request,"You Updated Placement Succesfully!")
                else:
                    messages.success(request,"Sorry This Dorm Full Place another place!")
            # print(blockk.id)
           

    return render(request,'StudentDean/updateStudent.html',context)
@login_required(login_url='login_view')
def export_users_csv(request):
    workbook=openpyxl.Workbook()
    worksheet=workbook.active
    worksheet['A1']='Id_no'
    worksheet['B1']='Gender'
    worksheet['C1']='Block'
    worksheet['D1']='Dorm'
   
    order=['Block_id','Room_id']
    pl=Placement.objects.all().order_by(*order)
    for i in pl:
        acc=UserAccount.objects.get(id=i.Stud_id_id)
        usr=User.objects.get(id=acc.User_id)
        Id=usr.Id_no
        gender=usr.Gender
        blk=Block.objects.get(id=i.Block_id)
        block=blk.Block_name
        drm=Dorm.objects.get(id=i.Room_id)
        Room=str(drm.Dorm_name)
        worksheet.append([Id,gender,block,Room])

    filename='Placement_Result.xlsx'
    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response=HttpResponse(content_type=content_type)
    response['Content-Disposition']=f'attchment; filename="{filename}"'
    workbook.save(response)
    return response

    
@login_required(login_url='login_view')
def delateStudent(request,pk):
    if 'username' in request.session:
        result=Placement.objects.get(id=pk)
        result.delete() 
        messages.error(request,"Student removed Succesfully!")
        return redirect('managePlacement')
    else:
        return redirect('login_view')
    return redirect('managePlacement')

@login_required(login_url='login_view')
def resetPlacement(request):
    if 'username' in request.session:
        orderlist=['Block_id','Room_id']
        result=Placement.objects.all().order_by(*orderlist)
        # for i in result:
        #     print(i.Block)
        S_Block=[]
        S_Room=[]
        Stud=[]
        ##########
        Room=[]
        block=[]
        User_acc=[]
        user_id=[]
        count=0
        for i in result:
            block.append(i.Block_id)
            Room.append(i.Room_id)
            
            usr=User.objects.get(id=i.Stud_id_id)
            Stud.append(usr)

            blk=Block.objects.get(id=block[count])
            S_Block.append(blk.Block_name)
            rm=Dorm.objects.get(id=Room[count])
            S_Room.append(rm.Dorm_name)
            count+=1

        lst=[{'item1':t[0],'item2':t[1],'item3':t[2]} for t in zip(Stud,S_Block,S_Room)] 
        context={'List':lst}
        setting=settings()
        context={**context,**setting}
        if request.method=='POST':
            searched=request.POST['searched']
            result1=Placement.objects.all()
            result=User.objects.filter(Department__contains=searched)| User.objects.filter(Id_no=searched)
            user_id=[]
            Block_name1=[]
            Dorm_name1=[]
            if result != "":
                for i in result:
                    # if UserAccount.objects.filter(User_id=i.id).exists():
                    #     acc=UserAccount.objects.get(User_id=i.id)
                    if Placement.objects.filter(Stud_id_id=i.id).exists():
                        pl=Placement.objects.get(Stud_id_id=i.id)
                        user_id.append(i)
                        blk=Block.objects.get(id=pl.Block_id)
                        drm=Dorm.objects.get(id=pl.Room_id)
                        Dorm_name1.append(drm.Dorm_name)
                        Block_name1.append(blk.Block_name)
                lst=[{'item1':t[0],'item2':t[1],'item3':t[2],'item4':t[3]} for t in zip(user_id,Block_name1,Dorm_name1,result1)] 
                context={'List':lst}
                setting=settings()
                context={**context,**setting}
            if Block.objects.filter(Block_name=searched).exists():
                block=Block.objects.get(Block_name=searched)
                
                if Placement.objects.filter(Block_id=block.id).exists():
                    
                    pl=Placement.objects.filter(Block_id=block.id)
                    for i in pl:  
                        Block_name1.append(block.Block_name)
                        # uracc=UserAccount.objects.get(id=i.Stud_id_id)
                        drm1=Dorm.objects.get(id=i.Room_id)
                        Dorm_name1.append(drm1.Dorm_name)
                        usr=User.objects.get(id=i.Stud_id_id)
                        user_id.append(usr)
                lst=[{'item1':t[0],'item2':t[1],'item3':t[2],'item4':t[3]} for t in zip(user_id,Block_name1,Dorm_name1,result1)] 
                context={'List':lst}
                setting=settings()
                context={**context,**setting}
            return render(request, "StudentDean/resetPlacement.html",context)

    else:
        return redirect('login_view')
    return render(request,'StudentDean/resetPlacement.html',context)
@login_required(login_url='login_view')
def delete_placement(request):
    if request.method =='POST':
        StudentId=request.POST.getlist('users')
        count=0
        count1=0
        for i in StudentId:
            usr=User.objects.get(Id_no=i)
            if UserAccount.objects.filter(User_id=usr.id).exists():
                acc=UserAccount.objects.get(User_id=usr.id)
                if Material.objects.filter(student_id=acc.id):
                    count1+=1
                    continue
            plc=Placement.objects.get(Stud_id_id=usr.id)
            plc.delete()
            count+=1
        # if count1 !=0:
        if count==0:
            if count1 !=0:
                msg="You can't Reset "+ str(count1)+" Students Placement Because they didn't return material"
                messages.error(request,msg)
            else:
                messages.error(request,"You Did not Select Student to Reset!")
        elif count==1:
            if count1 !=0:
                msg="You Have Reset one Student Placement Succesfully! But You can't Reset "+ str(count1)+" Students Placement Because they didn't return material"
                messages.error(request,msg)
            else:
                messages.success(request,"You Have Reset one Student Placement Succesfully!")
        else:
            if count1 !=0:
                msg="You Have Reset" + str(count)+ "Students Placement Succesfully! But You can't Reset "+ str(count1)+" Students Placement Because they didn't return material"
                messages.error(request,msg)
            else:
                msg="You Succesfully Reset "+ str(count)+" Students Placement!"
                messages.info(request,msg)
        return redirect('resetPlacement')
    return redirect('resetPlacement')
            
def rPlacement(request):
    if 'username' in request.session:
        #work here
        pass
    else:
        return redirect('login_view')
    return redirect('resetPlacement')
class PasswordsChangeView(PasswordChangeView):
    # from_class=PasswordChangeForm
    # form_class=PasswordChangingForm
    success_url=reverse_lazy('logout')
def logout_View(request):
    logout(request)
    #del request.session['username']
    return redirect('index')

