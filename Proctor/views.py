import csv
import openpyxl
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
from Proctor.forms import Property_Register_Form
from Supervisor.models import ProctorAssignment
from account.models import UserAccount,User,Settings
from StudentDean.models import Placement,Block,Dorm
from .models import Borrow_Request,Material,Properties,Exit_Permission_Requst,Exit_Permission
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from datetime import date

def settings():
    company=Settings.objects.all()
    for i in company:
        name=i.Abrevation_name
        context1={'Abrevation_name':name}
    return context1
# Create your views here.
@login_required(login_url='login_view')
def index(request):
    if 'username' in request.session:
        pass 
    else:
        return redirect('login_view')
    setting=settings()
    return render(request,"Proctor/index.html",setting)
@login_required(login_url='login_view')
def confirm_request(request,pk):
    if 'username' in request.session:
        student=User.objects.get(id=pk)
        student_acc=UserAccount.objects.get(User_id=student.id)
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        if ProctorAssignment.objects.filter(user_id=key).exists():
            if Borrow_Request.objects.filter(student_id=student_acc.id).exists():
                materials=Borrow_Request.objects.filter(student_id=student_acc.id)
                for i in materials:
                    obj1=Material(student_id=student_acc.id,proctor_id=key,property_id=i.property_id)
                    obj2=Borrow_Request.objects.get(property_id=i.property_id,student_id=student_acc.id)
                    
                    # print(obj2.id)
                    obj1.save()
                    obj2.delete()
                messages.info(request,'Succesfully Confirmed!')
            else:
               messages.info(request,'This Student is not Apply for Materials!') 
        else:
            messages.info(request,'You are not Assigned to any Dorm yet!')
    else:
        return redirect('login_view')
    return redirect('borrow_material')
@login_required(login_url='login_view')
def decline_material_request(request,pk):
    if 'username' in request.session:
        student=User.objects.get(id=pk)
        student_acc=UserAccount.objects.get(User_id=student.id)
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        if ProctorAssignment.objects.filter(user_id=key).exists():
            if Borrow_Request.objects.filter(student_id=student_acc.id).exists():
                obj2=Borrow_Request.objects.filter(student_id=student_acc.id)
                obj2.delete()
                messages.info(request,'Succesfully Cancled!')
            else:
               messages.info(request,'This Student is not Apply for Materials!') 
        else:
            messages.info(request,'You are not Assigned to any Dorm yet!')
    else:
        return redirect('login_view')
    return redirect('borrow_material')
#########Confimation Page########
@login_required(login_url='login_view') 
def borrow_material(request):
    if 'username' in request.session:
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        context={}
        if ProctorAssignment.objects.filter(user_id=key).exists():
            proctor=ProctorAssignment.objects.get(user_id=key)
            tt=proctor.Block_id
            block=Block.objects.get(id=tt)
            place=Placement.objects.filter(Block_id=tt).order_by('Room_id')
            accs=[]
            studs_id=[]
            student=[]
            room=[]
            Room1=[]
            status=[]
            for i in place:
                if Material.objects.filter(student_id=i.Stud_id_id).exists():
                    pass
                else:
                    accs.append(i.Stud_id_id)
                    room.append(i.Room_id)
                    if Borrow_Request.objects.filter(student_id=i.Stud_id_id).exists():
                        status.append("Pending")
                    else:
                        status.append("Not Requested")
            for i in accs:
                usr=User.objects.get(id=i)
                student.append(usr)
            for i in room:
                rm=Dorm.objects.get(id=i)
                Room1.append(rm)
            lst=[{'item1':t[0],'item2':t[1],'item3':t[2]} for t in zip(student,Room1,status)] 
            context={'List':lst,"Block":block}
        else:
            messages.info(request,"You Don't have been assigned to a block Yet")
    else:
        return redirect('login_view')
    setting=settings()
    context={**context,**setting}
    return render(request,'Proctor/borrow_material.html',context)
########Exit Permission#########
@login_required(login_url='login_view') 
def exit_permission_requests(request):
    if 'username' in request.session:
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        context={}
        if ProctorAssignment.objects.filter(user_id=key).exists():
            proctor=ProctorAssignment.objects.get(user_id=key)
            tt=proctor.Block_id
            block=Block.objects.get(id=tt)
            place=Placement.objects.filter(Block_id=tt)
            req=[]
            for i in place:                
                if Exit_Permission_Requst.objects.filter(student_id=i.Stud_id_id).exists():
                    result1=Exit_Permission_Requst.objects.get(student_id=i.Stud_id_id)
                    today=date.today()
                    if result1.date==today:
                        req.append(result1)
                    else:
                        result1.delete()
            # for i in req:
            #     print(i.student)
            context={'result':req}
        setting=settings()
        context={**context,**setting}
    else:
        return redirect('login_view')
    return render(request,'Proctor/exit_requests.html',context)
@login_required(login_url='login_view')
def accept_exit_request(request,pk):
    if 'username' in request.session:
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        obj=Exit_Permission_Requst.objects.get(id=pk)
        id=obj.student_id
        mat=obj.materials
        today=date.today()
        obj1=Exit_Permission(student_id=id,proctor_id=key,materials=mat,date=today)
        obj1.save()
        obj.delete()
    else:
        return redirect('login_view') 
    return redirect('exit_requests')
@login_required(login_url='login_view')
def decline_request(request,pk):
    if 'username' in request.session:
        obj=Exit_Permission_Requst.objects.get(id=pk)
        obj.delete()
    else:
        return redirect('login_view')
    return redirect('exit_requests')
################Student Information############
@login_required(login_url='login_view')       
def student_info(request):
    if 'username' in request.session:
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        context={}
        if ProctorAssignment.objects.filter(user_id=key).exists():
            proctor=ProctorAssignment.objects.get(user_id=key)
            tt=proctor.Block_id
            block=Block.objects.get(id=tt)
            place=Placement.objects.filter(Block_id=tt).order_by('Room_id')
            accs=[]
            studs_id=[]
            student=[]
            room=[]
            Room1=[]
            Status=[]
            for i in place:
                accs.append(i.Stud_id_id)
                room.append(i.Room_id)
            for i in accs:
                usr1=User.objects.get(id=i)
                student.append(usr1)
                if UserAccount.objects.filter(User_id=usr1.id).exists():
                    usr=UserAccount.objects.get(User_id=usr1.id)
                    if Material.objects.filter(student_id=usr.id).exists():
                        Status.append("Registered")
                    else:
                        Status.append("UnRegistered")
                else:
                    Status.append("UnRegistered")
            for i in room:
                rm=Dorm.objects.get(id=i)
                Room1.append(rm)
            lst=[{'item1':t[0],'item2':t[1],'item3':t[2]} for t in zip(student,Room1,Status)] 
            context={'List':lst,"Block":block}
        else:
            messages.info(request,"You Don't have been assigned to a block Yet")
    else:
        return redirect('login_view')
    setting=settings()
    context={**context,**setting}
    return render(request,'Proctor/student_info.html',context)
@login_required(login_url='login_view')     
def return_material(request,pk):
    # print(pk)
    acc=UserAccount.objects.get(User_id=pk)
    obj=Material.objects.filter(student_id=acc.id)
    for i in obj:
        print(i.id)
        i.delete()
    messages.success(request,"Student Reterned All Material He Borrowed!")
    return redirect('Student')
##############change Password##########
class PasswordsChangeView(PasswordChangeView):
    from_class= PasswordChangeForm
    template_name='Proctor/change_password.html'
    success_url=reverse_lazy('logout')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        setting=settings()
        context={**context,**setting}
        return context
##################Problem Report###############

from .models import ReportProblem
def report_view(request):

    if 'username' in request.session:  
        username=request.session['username']
        acc=UserAccount.objects.get(username=username)
        lst=[]
        us=[]
        ud=[]

        user=ProctorAssignment.objects.get(user=acc.id)
        if ReportProblem.objects.filter(is_solve='Un-Approved').exists():
          report=ReportProblem.objects.filter(is_solve='Un-Approved')
          for i in report:
              acc=UserAccount.objects.get(id=i.student_id)
              usr=User.objects.get(id=acc.User_id)
              if Placement.objects.filter(Stud_id_id=usr.id).exists():
                  stud=Placement.objects.get(Stud_id_id=usr.id)
                  if stud.Block==user.Block:
                      print(stud.Stud_id)
                      
                    #   print(aa)
                    #   u=User.objects.get(id=aa.id)
                      ud.append(stud)
                      lst.append(i)
                      us.append(stud)
        ls=[{'item1':t[0],'item2':t[1],'item3':t[2]} for t in zip(lst,us,ud)]               

        context={'Problem':ls}

    return render(request,'Proctor/view_report_problem.html',context)
def all_report_view(request):
     if 'username' in request.session:  
        username=request.session['username']
        acc=UserAccount.objects.get(username=username)
        lst=[]
        us=[]

        user=ProctorAssignment.objects.get(user=acc.id)
        if ReportProblem.objects.filter(is_solve='Approved').exists():
          report=ReportProblem.objects.filter(is_solve='Approved')
          
          for i in report:
                acc=UserAccount.objects.get(id=i.student_id)
                usr=User.objects.get(id=acc.User_id)
                if Placement.objects.filter(Stud_id_id=usr.id).exists():
                    stud=Placement.objects.get(Stud_id_id=usr.id)
                    if stud.Block==user.Block:
                        lst.append(i)
                        us.append(stud)
        ls=[{'item1':t[0],'item2':t[1]} for t in zip(lst,us)]               

        context={'Problem':ls}
     return render(request,'Proctor/view_all_report_problem.html',context)
###################Register Materials###########
@login_required(login_url='login_view')
def register_material(request):
    if 'username' in request.session:
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        context={}
        if ProctorAssignment.objects.filter(user_id=key).exists():
            proctor=ProctorAssignment.objects.get(user_id=key)
            tt=proctor.Block_id
            block=Block.objects.get(id=tt)
            block_name=block.Block_name
            dorm=Dorm.objects.filter(Block_id=block.id)
            context={'block_name':block_name,'dorm':dorm}
            setting=settings()
            context={**context,**setting}
            if request.method=='POST':
                pro_id=request.POST['property_id']
                pro_name=request.POST['Propery_name']
                block_name1=request.POST['Block_name']
                dorm_id=request.POST['Dorm_name']
                category=request.POST['category']
                if Properties.objects.filter(room_id=dorm_id,Propery_name=pro_name).exists() or Properties.objects.filter(Property_id=pro_id).exists() :
                    messages.error(request,'This Property is Already Registered!')
                    
                else:
                    block=Block.objects.get(Block_name=block_name1)
                    obj=Properties(Property_id=pro_id,Propery_name=pro_name,property_category=category,block_id=block.id,room_id=dorm_id)
                    obj.save()
                    messages.success(request,'This Property is Registered Succefully!')
                    return redirect("register_material")

        else:
            messages.info(request,'You are not Assigned to any Dorm yet!')
            
    else:
        return redirect('login_view')
    return render(request,'Proctor/register_material.html',context)
@login_required(login_url='login_view')
def borrowed_materials(request,pk):
    usr=User.objects.get(id=pk)
    user=UserAccount.objects.get(User_id=pk)
    if Material.objects.filter(student_id=user.id).exists():
        matt=[]
        materials=Material.objects.filter(student_id=user.id)
        for i in materials:
            obj=Properties.objects.get(id=i.property_id)
            matt.append(obj)
        return render(request,'Proctor/borrowed_materials.html',{'result':matt,'user':usr})
    else:
        messages.info(request, "This Student Doesn't Take any Material!")
    context={'user':usr}
    setting=settings()
    context={**context,**setting}
    return render(request,'Proctor/borrowed_materials.html',context)
@login_required(login_url='login_view')
def view_Materials(request):
    if 'username' in request.session:
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        if ProctorAssignment.objects.filter(user_id=key).exists():
            blk=ProctorAssignment.objects.get(user_id=key)
            block=blk.Block
            block1=Block.objects.get(Block_name=block)
            proprty=Properties.objects.filter(block_id=block1.id).order_by('room_id')
            dorm=[]
            for i in proprty:
                drm=Dorm.objects.get(id=i.room_id)
                dorm.append(drm.Dorm_name)
            lst=[{'item1':t[0],'item2':t[1]} for t in zip(proprty,dorm)] 
            context={'result':lst,'Block':block}
            return render(request,'Proctor/View_materials.html',context)
        else:
            messages.error(request,'You Are not Assigned to any Dorm Yet')
    else:
        return redirect('login_view')
    setting=settings()
    return render(request,'Proctor/View_materials.html',setting)
@login_required(login_url='login_view')
def search_material(request):
    if request.method=="POST":
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        context={} 
        if ProctorAssignment.objects.filter(user_id=key).exists():
            blk=ProctorAssignment.objects.get(user_id=key)
            block=blk.Block
            block1=Block.objects.get(Block_name=block)
            searched=request.POST["searched"]
            if Dorm.objects.filter(Dorm_name=searched,Block_id=block1.id).exists():
                dorm=Dorm.objects.get(Dorm_name=searched,Block_id=block1.id)
                if Properties.objects.filter(room_id=dorm.id).exists():
                    proprty=Properties.objects.filter(room_id=dorm.id)
                    dorm=[]
                    for i in proprty:
                        drm=Dorm.objects.get(id=i.room_id)
                        dorm.append(drm.Dorm_name)
                    lst=[{'item1':t[0],'item2':t[1]} for t in zip(proprty,dorm)] 
                    context={'result':lst,'Block':block}
                    return render(request,'Proctor/View_materials.html',context)
                else:
                    messages.info(request,"This dorm have no Material")
            else:
                messages.info(request,"This Dorm is not in this Block")
                return redirect("view_Materials")
        else:
            messages.info(request,"You are not Assigned to any Dorm yet!")

        setting=settings()
        context={**context,**setting} 
        return render(request, 'Proctor/View_materials.html',context)   
    setting=settings()
    return render(request,'Proctor/View_materials.html',setting)
@login_required(login_url='login_view')
def Import_materials(request):
    if 'username' in request.session:
        username = request.session['username']
        idd=UserAccount.objects.get(username=username)
        key=idd.id
        if ProctorAssignment.objects.filter(user_id=key).exists():
            count=0
            try:
                
                if request.method == 'POST' and request.FILES['myfile']: 
                    category=request.POST['category']
                    if category =="":
                        messages.info(request,"Please Select materials Category!")
                        return redirect('')
                    else:
                        # block_type_id=BlockType.objects.get(Block_Type=blocktype)
                        
                        myfile = request.FILES['myfile']             
                        empexceldata = pd.read_excel(myfile)        
                        dbframe = empexceldata
                        
                        for dbframe in dbframe.itertuples():
                            
                        
                            if Properties.objects.filter(Property_id=dbframe.Property_id).exists():          
                                continue
                            else:
                                # adding 00 to Dorm name is not conventional!
                                room=str(dbframe.room)
                                if len(room)==1:
                                    room='00'+room
                                shced=ProctorAssignment.objects.get(user_id=key)
                                block_id=shced.Block_id
                                rm=Dorm.objects.get(Block_id=block_id,Dorm_name=room)
                                room_id=rm.id
                                obj=Properties.objects.create(Property_id=dbframe.Property_id,Propery_name=dbframe.Propery_name,property_category=category,block_id=block_id,room_id=room_id)
                                obj.save()  
                                count+=1           
                        if count==0:
                            messages.warning(request,"All Material Id's are Already Registered...!")
                        elif count==1:
                            messages.success(request,"One Material is Registered Succesfully...!")
                        else:
                            mess=str(count)+" Materials  added successfuly...!!"
                            messages.success(request,mess)
            except:
                msg= 'Error Occured after Inserting '+str(count) +' Data Please Correct Your the table'
                messages.error(request,msg)

        else:
            messages.error(request,'You Are not Assigned to any Dorm Yet')
    else:
        return redirect('login_view')  
    setting=settings() 
    return render(request, 'Proctor/upload_materials.html',setting)
@login_required(login_url='login_view')
def edit_material(request,pk):
    result=Properties.objects.get(id=pk)
    # result1=Block.objects.all()
    form=Property_Register_Form(request.POST or None,instance=result)
    context = { 'res': result,'form':form} 
    setting=settings()
    context={**context,**setting}
    if form.is_valid():
        form.save()
        messages.success(request,"Data Updated Succesfully!")
        return redirect("view_Materials")
    return render(request,'Proctor/updatematerial.html',context)

@login_required(login_url='login_view')
def delete_material(request,pk):
    obj=Properties.objects.get(id=pk)
    obj.delete()
    return redirect('view_Materials')
@login_required(login_url='login_view')
def download_excel(request):
    workbook=openpyxl.Workbook()
    worksheet=workbook.active
    worksheet['A1']='Property_id'
    worksheet['B1']='Propery_name'
    worksheet['C1']='room'
    filename='bulk_properties.xlsx'
    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response=HttpResponse(content_type=content_type)
    response['Content-Disposition']=f'attchment; filename="{filename}"'
    workbook.save(response)
    return response
@login_required(login_url='login_view')
def logout_View(request):
    logout(request)
    #del request.session['username']
    return redirect('index')
