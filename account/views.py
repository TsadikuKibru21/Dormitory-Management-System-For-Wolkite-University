from django.contrib.auth import authenticate,logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import UserAccount,User,Role,ArchieveAccount
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import *
from django.contrib.auth.hashers import make_password
import datetime as dt
import pandas as pd
import os
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
# Create your views here.
def account_activate_deactivate(request):
    if request.method=='POST':
        id=request.POST['user_id']
        acc=UserAccount.objects.get(id=id)
        if acc.is_active:
            acc.is_active=False
        else:
            acc.is_active=True
        acc.save()
    return redirect('grantrole')
def settings():
    company=Settings.objects.all()
    for i in company:
        name=i.Abrevation_name
        context1={'Abrevation_name':name}
    return context1
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def adminhome(request):
    if 'username' in request.session:
        company=Settings.objects.all()
        for i in company:
            name=i.Abrevation_name
        if request.session['username']=="":  
            redirect('login_view')
        Role_list=['StudentDean','Student','Proctor','Supervisor','Admin','President','Registrar','Employee']
        for i in range(8):
            if Role.objects.filter(R_name=Role_list[i]).exists():
                user=Role.objects.get(R_name=Role_list[i])
                pass
            else:
                role=Role()
                role.R_name=Role_list[i]
                role.save()
    else:
        return redirect('login_view')
    
    return render(request,"account/index.html",{"Abrevation_name":name})
@login_required(login_url='login_view')
def update_setting(request):
    if 'username' in request.session:
        company = Settings.objects.all()
        pk = ''
        for i in company:
            pk = i.company_name
            break

        try:
            result = Settings.objects.get(company_name=pk)
        except Settings.DoesNotExist:
            # Handle the case where no matching record is found
            # You may want to display an error message or redirect to an appropriate page.
            pass

        if request.method == 'POST':
            form = UpdateSettingForm(request.POST, request.FILES, instance=result)
            if form.is_valid():
                form.save()
                messages.success(request, "Data Updated Successfully!")
                return redirect('LAdmin')
        else:
            form = UpdateSettingForm(instance=result)

        context = {'res': result, 'form': form}
        setting = settings()
        context = {**context, **setting}
    else:
        return redirect('login_view')
    return render(request, 'account/updatesetting.html', context)

#################Account Managment###############
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def accountmanagment(request):
    if 'username' in request.session:
        result=User.objects.order_by("Id_no")
        user=User.objects.all().count()
        acc=UserAccount.objects.all().count()
        lst=[]
        for i in result:
            if UserAccount.objects.filter(User_id=i.id).exists():
                pass
            else:
                lst.append(i)
        
        context={"User":lst,'AvUser':user,'Account':acc}
        setting=settings()
        context={**context,**setting}
        # print(user,acc)
    else:
        return redirect('login_view')
    return render(request,"account/accountmanagment.html",context)
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def generateuseraccount(request):
    if 'username' in request.session:
        
        result=User.objects.order_by("Id_no")
        user=User.objects.all().count()
        acc=UserAccount.objects.all().count()
        context={"User":result,'AvUser':user,'Account':acc}
        setting=settings()
        context={**context,**setting}
        if request.method == "POST":
            selectedusers=request.POST.getlist("users")
            count=0 
            for rs in selectedusers:
                user=User.objects.get(Id_no=rs)
                useracc=UserAccount()
                # username=user.FirstName+user.LastName
                
                ####password username are both Id number
                if UserAccount.objects.filter(username=rs).exists():
                    pass
                else:
                    count+=1
                    if ArchieveAccount.objects.filter(username=rs).exists():
                        obj1=ArchieveAccount.objects.get(username=rs)
                        r_id=0
                        if user.is_Employee:
                            r=Role.objects.get(R_name="Employee")
                            r_id=r.id
                        else:
                            r=Role.objects.get(R_name="Student")
                            r_id=r.id
                        useracc.username=rs
                        useracc.password=obj1.password
                        useracc.Role_id=r_id
                        useracc.User_id=int(user.id)
                        useracc.save()
                    else:
                        useracc.username=rs
                        password=make_password(rs)
                        useracc.password=password
                        if user.is_Employee:
                            role=Role.objects.get(R_name='Employee')
                        else:
                            role=Role.objects.get(R_name='Student')
                        useracc.Role_id=role.id
                        useracc.User_id=int(user.id)
                        useracc.save()
                        
            
            if count ==0:
                messages.info(request,"All users Already have An Account!")
            elif count==1:
                mess=str(count)+" User Account is Succesfully created"
                messages.success(request,mess)
            else:
                mess=str(count)+" User's Account is Succesfully created"
                messages.success(request,mess)
            
            return redirect('accountmanagment')
    else:
        return redirect('login_view')      
    return render(request,'account/accountmanagment.html',context)

@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def GrantRole(request):
    if 'username' in request.session:
        result=[]
        usr=User.objects.all()

        for i in usr:
            if i.is_Employee:
                rs=UserAccount.objects.get(User_id=i.id)
                result.append(rs)
        if request.method =='POST':
            searched=request.POST['searched']
            
            if searched =='Student':
                role=Role.objects.get(R_name="Student")
                id=role.id
            elif searched == 'StudentDean':
                role=Role.objects.get(R_name="StudentDean")
                id=role.id
            elif searched == 'Admin':
                role=Role.objects.get(R_name="Admin")
                id=role.id
            elif searched == 'Proctor':
                role=Role.objects.get(R_name="Proctor")
                id=role.id
            elif searched == 'Supervisor':
                role=Role.objects.get(R_name="Supervisor")
                id=role.id
            elif searched == 'President':
                role=Role.objects.get(R_name="President")
                id=role.id
            elif searched == 'Registrar':
                role=Role.objects.get(R_name="Registrar")
                id=role.id
            else:
                id=0
            result=UserAccount.objects.filter(username__contains=searched)| UserAccount.objects.filter(Role=id)
            context={'Account':result}
            setting=settings()
            context={**context,**setting}
            return render(request, "account/grantrole.html",context)
    else:
        return redirect('login_view')
    context={'Account':result}
    setting=settings()
    context={**context,**setting}
    return render(request, "account/grantrole.html",context)
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def updaterole(request,pk):
    if 'username' in request.session:
        result=UserAccount.objects.get(id=pk)
        result1=UserAccount.objects.all()
        form=AddAccountForm(request.POST or None,instance=result)
        context = { 'form':form}
        setting=settings()
        context={**context,**setting}
        if form.is_valid():
            form.save()
            messages.success(request,"Data Updated Succesfully!")
            context={"Account":result1}
            setting=settings()
            context={**context,**setting}
            return redirect('grantrole')
    else:
        return redirect('login_view')
    return render(request,'account/updaterole.html',context)
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def AddUser(request):
    if 'username' in request.session:
        form=AddUserForm(request.POST or None)
        if request.method=='POST':
            if form.is_valid():
                Id_no=request.POST['Id_no']
                if User.objects.filter(Id_no=Id_no).exists():
                    messages.info(request,'This User is Already Registered!...')
                    return redirect('Ad_adduser')
                else:
                    form.save()
                    messages.info(request,'User Added Succesfully!...')
                    return redirect('Ad_adduser')
            else:
                messages.info(request,'Invalid Form! Please Fulfill Requirements!')
    else:
        return redirect('login_view')
    context={'form':form}
    setting=settings()
    context={**context,**setting}
    return render(request, "account/adduser.html",context)
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def userinfo(request):
    if 'username' in request.session:
        result=User.objects.order_by("FirstName")
    else:
        return redirect('login_view')
    context={"User":result}
    setting=settings()
    context={**context,**setting}
    return render(request,"account/viewuserinfo.html",context)
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def deleteuser(request):
    if 'username' in request.session:
        result=User.objects.order_by("FirstName")
        if request.method == "POST":
            selectedusers=request.POST.getlist("users")
        #print(selectedusers)
            count=0 
            for rs in selectedusers:
                user=User.objects.get(Id_no=rs)
                if UserAccount.objects.filter(User_id=user.id).exists():
                    acc=UserAccount.objects.get(User_id=user.id)
                    if ArchieveAccount.objects.filter(username=acc.username).exists():
                        obj1=ArchieveAccount.objects.get(username=acc.username)
                        obj1.password=acc.password
                        obj1.save()
                    else:
                        obj2=ArchieveAccount(username=acc.username,password=acc.password)
                        obj2.save()
                user.delete() 
                count+=1
            mess=str(count)+" User's Deleted Succesfully!..."
            messages.error(request,mess)
    else:
        return redirect('login_view')
    context={"User":result}
    setting=settings()
    context={**context,**setting}
    return render(request,"account/viewuserinfo.html",context)
 
def export_users_csv(request):
    
     
    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Users.csv"'        
        writer = csv.writer(response)
        writer.writerow(['Users Detail'])       
                 
         
        writer.writerow(['Id_no','FirstName','LastName','Gender','phone_no','stream','collage','Department' ,'Year_of_Student' ,'Emergency_responder_name','Disability'])
 
        users = User.objects.all().values_list('Id_no','FirstName' , 'LastName' , 'Gender','phone_no','stream','collage','Department' ,'Year_of_Student','Emergency_responder_name','Disability')
         
        for user in users:
            writer.writerow(user)
        return response
    setting=settings()
    
    return render(request, 'account/exportexcel.html',setting)



class PasswordsChangeView(PasswordChangeView):
    from_class= PasswordChangeForm
    template_name='account/change_password.html'
    success_url=reverse_lazy('logout')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        setting=settings()
        context={**context,**setting}
        return context
@login_required(login_url='login_view')
def reset_password(request):
    if request.method=='POST':
        username=request.POST.get('username1')
        new_password=request.POST.get('password')
        # print(username,new_password)
        if UserAccount.objects.filter(username=username).exists():
            user=UserAccount.objects.get(username=username)
            password=make_password(new_password)
            user.password=password
            user.save()
            messages.info(request,"Password reset Succesfully!")
            return redirect('password_reset')
        else:
            messages.info(request, 'There is no Username Like this Try Another!')
            return redirect('password_reset')
    setting=settings()
    return render(request,'account/reset_password.html',setting)

@login_required(login_url='login_view')
def logout_View(request):
    logout(request)
    #del request.session['username']
    return redirect('index')