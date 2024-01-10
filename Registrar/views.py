from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, View
import csv,openpyxl, pandas as pd
from django.contrib import messages
from Registrar.forms import StudentForm
from account.models import User,UserAccount,BlockType
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from account.models import Settings
def settings():
    company=Settings.objects.all()
    for i in company:
        name=i.Abrevation_name
        context1={'Abrevation_name':name}
    return context1
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def index(request):
    if 'username' in request.session:
        company=Settings.objects.all()
        for i in company:
            name=i.Abrevation_name 
    else:
        return redirect('login_view')
    return render(request,'Registrar/index.html',{"Abrevation_name":name})
###################USER REGISTRATION###################
@login_required(login_url='login_view')
@csrf_exempt
def Adduser(request):
    if 'username' in request.session:
        serializer = UserSerializer()
        context ={
            'serializer': serializer
        }
        if request.method == 'GET':
            return render(request,'Registrar/adduser.html',context)
    else:
        return redirect('login_view')
    return JsonResponse(serializer.errors, status=400)
@login_required(login_url='login_view')
@api_view(['POST'])
def Adduser1(request):
    if 'username' in request.session:
        serializer = UserSerializer(data=request.data)
        a=request.data
        if serializer.is_valid():
                if User.objects.filter(Id_no=a['Id_no']).exists() :
                    messages.error(request,'A User With This ID is Already Registered...!!')
                    return redirect('adduser')
                serializer.save()
                messages.success(request,'User Registered successfuly...!!')
                return redirect('adduser')
        else:
                messages.error(request,'Insert the Necessary information Data...!!')
                return redirect('adduser')
    else:
        return redirect('login_view')           
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
    return render(request, 'Registrar/uploadusers.html',{'block_type':block_type})
@login_required(login_url='login_view')
def download_excel(request):
    workbook=openpyxl.Workbook()
    worksheet=workbook.active
    worksheet['A1']='Id_no'
    worksheet['B1']='FirstName'
    worksheet['C1']='LastName'
    worksheet['D1']='Gender'
    worksheet['E1']='phone_no'
    worksheet['F1']='stream'
    worksheet['G1']='collage'
    worksheet['H1']='Department'
    worksheet['I1']='Year_of_Student'
    worksheet['J1']='Disability'
    worksheet['K1']='Emergency_responder_name'
    worksheet['L1']='Emergency_responder_address'
    worksheet['M1']='Emergency_responder_phone_no'

    filename='Students.xlsx'
    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response=HttpResponse(content_type=content_type)
    response['Content-Disposition']=f'attchment; filename="{filename}"'
    workbook.save(response)
    return response
@login_required(login_url='login_view')
def viewStudent(request):
    if 'username' in request.session:
        usr=User.objects.all()
        user=[]
        for i in usr:
            if i.is_Employee:
                pass
            else:
                user.append(i)
        context={"User":user}
        setting=settings()
        context={**context,**setting}
    else:
        return redirect('login_view')
    return render(request,'Registrar/viewstudent.html',context)
@login_required(login_url='login_view')
def Edit_Students(request,pk):
    if 'username' in request.session:
        result=User.objects.get(id=pk)
        # result1=Announcement.objects.all()
        form=StudentForm(request.POST or None,instance=result)
        context = { 'res': result,'form':form} 
        if form.is_valid():
            form.save()
            messages.success(request,"Data Updated Succesfully!")
            return redirect('R_viewstudent')
            # return render(request ,'StudentDean/view_announce.html',{"Block":result1})
    else:
        return redirect('login_view')
    return render(request,'Registrar/Edit_Student.html',context)
def delete_student(request,pk):
    usr=User.objects.get(id=pk)
    usr.delete()
    return redirect("R_viewstudent")
class PasswordsChangeView(PasswordChangeView):
    from_class= PasswordChangeForm
    success_url=reverse_lazy('logout')
@cache_control(no_cache=True,must_revalidate=True)
@login_required(login_url='login_view')
def logout_View(request):
    logout(request)
    #del request.session['username']
    return redirect('index')