from django.shortcuts import render,redirect
from django.http import HttpResponse
from account.models import Settings
from django.contrib.auth.decorators import login_required
from StudentDean.models import Block,Dorm,Placement
from account.models import User,UserAccount
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy

def settings():
    company=Settings.objects.all()
    for i in company:
        name=i.Abrevation_name
        context1={'Abrevation_name':name}
    return context1
# Create your views here.
@login_required(login_url='login_view')
def presidenthome(request):
    if 'username' in request.session:
        company=Settings.objects.all()
        for i in company:
            name=i.Abrevation_name
    else:
        return redirect('login_view')
    return render(request,'President/index.html',{"Abrevation_name":name})


@login_required(login_url='login_view')
def give_permission(request):
    if 'username' in request.session:
        pass
    else:
        return redirect('login_view')
    return render(request,"President/give_permission.html")
@login_required(login_url='login_view')
def viewblock(request):
    if 'username' in request.session:
        result=Block.objects.order_by('Block_name')
    else:
        return redirect('login_view')
    context={"Block":result}
    setting=settings()
    context={**context,**setting}
    return render(request ,'President/viewblock.html',context)
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
    return render(request ,'President/viewdorm.html',context)

@login_required(login_url='login_view')
def View_placement(request):
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
            ##gatting user_account id from placement
            User_acc.append(i.Stud_id_id)
            userr=UserAccount.objects.get(id=User_acc[count])
            ##gatting user  id from Useraccount
            user_id.append(userr.User_id)
            ##gatting user it self
            usr=User.objects.get(id=user_id[count])
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
    else:
        return redirect('login_view')
    return render(request,"President/placementinfo.html",context)
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
            try:
                acc=UserAccount.objects.get(id=i.Stud_id_id)
                usr=User.objects.get(id=acc.User_id)
                if usr.Gender == 'Male':
                    placed_male+=1
                else:
                    placed_female+1
            except UserAccount.DoesNotExist:
                # Handle cases where the UserAccount does not exist
                print(f"UserAccount for Stud_id {i.Stud_id_id} not found.")
                continue  # Skip this placement and continue with the next
            
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
    return render(request,"President/dormitory_information.html",context)

##############change Password##########
class PasswordsChangeView(PasswordChangeView):
    from_class= PasswordChangeForm
    template_name='President/change_password.html'
    success_url=reverse_lazy('logout')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        setting=settings()
        context={**context,**setting}
        return context