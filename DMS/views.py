from django.conf import settings
from account.forms import LoginForm
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import User,Role,UserAccount,Settings
from django.contrib.auth.hashers import make_password
from Proctor.models import Exit_Permission_Requst

from django.utils.crypto import get_random_string
from django.core.mail import send_mail
def index(request):
    if User.objects.filter(Id_no='Admin').exists():
       
        pass
    else:
        user=User()
        user.FirstName="Admin"
        user.LastName="Admin"
        user.Id_no="Admin"
        user.Gender="Male"
        user.phone_no="123"
        user.save()
        
    if Role.objects.filter(R_name="Admin").exists():
        # print("role already added")
        pass
    else:
        role=Role()
        role.R_name="Admin"
        role.save()
        #print("role added")
    if UserAccount.objects.filter(username="AdminAdmin").exists():
        
        pass
    else:
        form=UserAccount()
        form.username="AdminAdmin"
        password=make_password("Admin")
        form.password=password
        form.Role=Role.objects.get(R_name="Admin")
        form.User=User.objects.get(Id_no="Admin")
        form.save()
        #print("accc added ")
    company=Settings.objects.all()
    for i in company:
        image=i.background_image
        break
    context={'settings':company,"image":image}
    return render(request,"index.html",context)
def login_view(request):
    form=LoginForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(username=username,password=password)
            company=Settings.objects.all()
            if user is not None:
                #role=user.Role
                role=str(user.Role)
                
                if role  == "Student_Dean":
                    request.session['username'] = username
                    for i in company:
                        request.session['company_name']=i.company_name
                    login(request, user)
                    return redirect('studentdeanhome')
                elif role=='Admin':
                    for i in company:
                        request.session['company_name']=i.company_name
                    request.session['username'] = username
                    login(request, user)
                    return redirect('LAdmin',)
                    #return render(request, 'account/index.html',{'username':username})
                elif role=='Student':
                    request.session['username'] = username
                    login(request,user)
                    return redirect('student')
                    #return render(request, 'account/index.html')
                elif role=='Proctor':
                    for i in company:
                        request.session['company_name']=i.company_name
                    request.session['username'] = username
                    login(request,user)
                    return redirect('proctor')
                elif role=='Supervisor':
                    for i in company:
                        request.session['company_name']=i.company_name
                    request.session['username'] = username
                    login(request,user)
                    return redirect('supervisor')
                elif role=='Registrar':
                    for i in company:
                        request.session['company_name']=i.company_name
                    request.session['username'] = username
                    login(request,user)
                    return redirect('Registrar')
                elif role=='President':
                    for i in company:
                        request.session['company_name']=i.company_name
                    request.session['username'] = username
                    login(request,user)
                    return redirect('president')
                else:
                    messages.error(request,"You have no Role In this System...")
            else:
                messages.error(request,"Invalid credientials...")
    company=Settings.objects.all()
    
    for i in company:
        image=i.background_image
        break
    context={'form':form,"settings":company,"image":image}  
    
    return render(request,'login.html',context)
def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            
            account=UserAccount.objects.get(User_id=user.id)
           
            # Generate a new password
            new_password = get_random_string(length=12)
          
            account.set_password(new_password)
            account.save()
          
            messages.success(request, 'Successfully send to email address.')
            # Send email notification
            send_mail('Password Reset Request',f'Your new password is: {new_password}',settings.EMAIL_HOST_USER,[email],fail_silently=False)

            return redirect('forget_password')
        except:
            messages.error(request, 'No user found with that email address.')
            return redirect('forget_password')
    return render(request, 'forget_password.html')