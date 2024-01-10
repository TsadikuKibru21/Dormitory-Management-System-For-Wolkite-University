import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from StudentDean.models import Block
from account.models import ChatMessage, UserAccount,User,Settings,Role
from .models import ProctorAssignment,schedule
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from datetime import date,timedelta,datetime
from random import shuffle
from itertools import cycle
import csv,openpyxl, pandas as pd
###############Settings##########
def settings():
    company=Settings.objects.all()
    for i in company:
        name=i.Abrevation_name
        context1={'Abrevation_name':name}
    return context1
# Create your views here.z
##############Schedule##########
def generate_schedule(proctor,start_date,end_date,number_of_shift_per_day):
    # print(proctor)
    start_date=datetime.strptime(start_date,'%Y-%m-%d').date()
    end_date=datetime.strptime(end_date,'%Y-%m-%d').date()
    proctors=list(proctor)
    shuffle(proctors)
    num_proctor=len(proctors)
    days=(end_date-start_date).days+1
    shifts=[]
    for i in range(1,number_of_shift_per_day+1):
        shifts.append("Shift"+ str(i))
    # print(shifts)
    nshifts=number_of_shift_per_day
    if ((num_proctor %2 == 0 and nshifts %2 ==0) or (num_proctor %2 == 1 and nshifts %2 ==1))and num_proctor>0:#even
        pr=0
        sh=0
        date=start_date - timedelta(days=1) #start date
        for i in range(nshifts*days):
            if i % num_proctor==0 and nshifts!=1:
                proctor.reverse()
            if i%nshifts==0:
                date=date + timedelta(days=1)
            obj=schedule()
            prt=UserAccount.objects.get(id=proctor[pr])
            obj.procotor=prt
            obj.date=date
            obj.shift=shifts[sh]
            obj.num_shift_per_day=nshifts
            obj.save()
            # print(shifts[sh]," proc=",proctor[pr])
            pr+=1
            sh+=1
            if pr==num_proctor:
                pr=0
            if sh==nshifts:
                sh=0
    elif ((num_proctor %2 == 0 and nshifts %2 ==1) or (num_proctor %2 == 1 and nshifts %2 ==0))and num_proctor>0:
        pr=0
        sh=0
        date=start_date - timedelta(days=1) #start dat
        # print(nshifts*days)
        for i in range(nshifts*days):
            if i%nshifts==0:
                date=date + timedelta(days=1)
            obj=schedule()
            prt=UserAccount.objects.get(id=proctor[pr])
            obj.procotor=prt
            obj.date=date
            obj.shift=shifts[sh]
            obj.num_shift_per_day=nshifts
            obj.save()
            # print(shifts[sh]," proc=",proctor[pr])
            pr+=1
            sh+=1
            if pr==num_proctor:
                pr=0
            if sh==nshifts:
                sh=0
@login_required(login_url='login_view')
def home(request):
    if 'username' in request.session:
        pass 
    else:
        return redirect('login_view')
    setting=settings()
    return render(request,'Supervisor/index.html',setting)
###########Assing Proctor to Dorms############
@login_required(login_url='login_view')
def assign_Block(request):
    if 'username' in request.session:
        block=Block.objects.order_by("Block_name")
        role=Role.objects.get(R_name='Proctor')
        proctor1=UserAccount.objects.filter(Role_id=role.id)
        proctor=[]
        Proctor_name=[]
        for i in proctor1:
            if ProctorAssignment.objects.filter(user_id=i.id).exists():
                pass
            else:
                proctor.append(i)
                usr=User.objects.get(id=i.User_id)
                full_name=usr.FirstName+ " "+ usr.LastName
                Proctor_name.append(full_name)
        lst=[{'item1':t[0],'item2':t[1]} for t in zip(proctor,Proctor_name)] 
        # context={'List':lst}
        context={"Block":block,"Proctor":lst}
        setting=settings()
        context={**context,**setting} 
        if request.method =='POST':
            proctor1=request.POST['proctor']
            block1=request.POST['block']
            proctor=UserAccount.objects.get(username=proctor1)
            Block1=Block.objects.get(Block_name=block1)
            usr=User.objects.get(id=proctor.User_id)
            proctor_sex=str(usr.Gender).lower()
            block_purpose=str(Block1.Block_purpose).lower()
            if proctor_sex in block_purpose:
                if ProctorAssignment.objects.filter(user_id=proctor.id).exists() or ProctorAssignment.objects.filter(Block_id=Block1).count()>=4:
                    messages.info(request,"This Proctor is Already Assigned or This Block Has Enuogh Proctor")
                    return redirect('assign_block')
                else:
                    obj=ProctorAssignment()
                    obj.user=proctor
                    obj.Block=Block1
                    obj.save()
                    sched=schedule.objects.all()
                    if len(sched)>0:
                        start_date=str(sched[0].date)
                        n=len(sched)
                        end_date=str(sched[n-1].date)
                        no_shifts=sched[0].num_shift_per_day
                        for i in sched:
                            ptr=ProctorAssignment.objects.get(user=i.procotor)
                            if Block1==ptr.Block:
                                dlsd=schedule.objects.get(id=i.id)
                                dlsd.delete()
                        proctor=ProctorAssignment.objects.filter(Block=Block1)
                        lst=[]
                        for i in proctor:
                            lst.append(i.user_id)
                        generate_schedule(lst,start_date,end_date,no_shifts)
                    messages.info(request,'Proctor Assigned Succesfully...')
                    return redirect('assign_block')
            else:
                messages.info(request,'User Gender and the Block Purpose does not Match!...')
                return redirect('assign_block')
    else:
        return redirect('login_view')
        
    return render (request,'Supervisor/assign_block.html',context)
#######View Assigned Proctors #############
@login_required(login_url='login_view')
def proctor_Info(request):
    if 'username' in request.session:
        result=ProctorAssignment.objects.all()
        Proctor_name=[]
        Userid=[]
        for i in result:
            acc=UserAccount.objects.get(username=i.user)
            usr=User.objects.get(id=acc.User_id)
            Userid.append(acc.id)
            full_name=usr.FirstName+ " "+ usr.LastName
            Proctor_name.append(full_name)
        lst=[{'item1':t[0],'item2':t[1],'item3':t[2]} for t in zip(result,Proctor_name,Userid)] 
        context={'Result':lst}
        setting=settings()
        context={**context,**setting}
    else:
        return redirect('login_view')
    return render(request,'Supervisor/proctor_info.html',context)
class PasswordsChangeView(PasswordChangeView):
    from_class= PasswordChangeForm
    template_name='Supervisor/change_password.html'
    success_url=reverse_lazy('logout')
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        setting=settings()
        context={**context,**setting}
        return context

        
def set_schedule(request):
    if 'username' in request.session:
        if request.method=='POST':
            start_date=request.POST['startdate']
            end_date=request.POST['enddate']
            no_shifts=int(request.POST['no_shifts'])
            obj=schedule.objects.all()
            obj.delete()
            block=Block.objects.all()
            for i in block:
                if ProctorAssignment.objects.filter(Block_id=i.id).exists():
                    proctor=ProctorAssignment.objects.filter(Block_id=i.id)
                    lst=[]
                    for i in proctor:
                        lst.append(i.user_id)
                    generate_schedule(lst,start_date,end_date,no_shifts)
            messages.info(request,"Schedule Setted Succesfully!")
    else:
        return redirect('login_view')
    context=settings()
    return render(request,"Supervisor/set_schedule.html",context)
def schedule_info(request):
    if 'username' in request.session:
        # all()
        result=schedule.objects.order_by('date','shift')
        block=[]
        Proctor_name=[]
        for i in result:
            # print(i.procotor_id)
            if ProctorAssignment.objects.filter(user_id=i.procotor_id).exists():
                pr=ProctorAssignment.objects.get(user_id=i.procotor_id)
                blk=Block.objects.get(id=pr.Block_id)
                acc=UserAccount.objects.get(username=i.procotor)
                usr=User.objects.get(id=acc.User_id)
                Fullname=usr.FirstName +" "+ usr.LastName
                Proctor_name.append(Fullname)
                block.append(blk.Block_name)
            # print(blk.Block_name)
        lst=[{'item1':t[0],'item2':t[1],'item3':t[2]} for t in zip(result,block,Proctor_name)] 
        context={'List':lst}
        setting=settings()
        context={**context,**setting}
    else:
        return redirect('login_view')
    return render(request,"Supervisor/view_schedule.html",context)
@login_required(login_url='login_view')
def export_proctor_schedule(request):
    workbook=openpyxl.Workbook()
    worksheet=workbook.active
    worksheet['A1']='Date'
    worksheet['B1']='Shift'
    worksheet['C1']='Proctor'
    worksheet['D1']='Block'
    order=['date','shift']
    pl=schedule.objects.all().order_by(*order)
    for i in pl:
        # print(i.procotor_id)
        date=str(i.date)
        shift=i.shift
        acc=UserAccount.objects.get(username=i.procotor)
        usr=User.objects.get(id=acc.User_id)
        Fullname=usr.FirstName +" "+ usr.LastName
        ass=ProctorAssignment.objects.get(user_id=i.procotor_id)
        blk=Block.objects.get(id=ass.Block_id)
        block=blk.Block_name
        worksheet.append([date,shift,Fullname,block])

    filename='Proctor Schedule.xlsx'
    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response=HttpResponse(content_type=content_type)
    response['Content-Disposition']=f'attchment; filename="{filename}"'
    workbook.save(response)
    return response
def update_Proctor_block(request,pk):
    block=Block.objects.order_by("Block_name")
    ass=ProctorAssignment.objects.get(user_id=pk)
    pr_block=ass.Block
    acc=UserAccount.objects.get(id =pk)
    usr=User.objects.get(id=acc.User_id)
    Full_name=usr.FirstName +" "+usr.LastName
    context={"name":Full_name,"Block":block,"currentB":pr_block}
    if request.method =='POST':
        # proctor1=request.POST['proctor']
        block1=request.POST['block']
        proctor=UserAccount.objects.get(id=pk)
        Block1=Block.objects.get(Block_name=block1)
        usr=User.objects.get(id=proctor.User_id)
        proctor_sex=str(usr.Gender).lower()
        block_purpose=str(Block1.Block_purpose).lower()
        if proctor_sex in block_purpose:
            if  ProctorAssignment.objects.filter(Block_id=Block1).count()>=4:
                messages.info(request," This Block Has Enuogh Proctor")
                return redirect('proctor_info')
            else:
                ss=ProctorAssignment()
                obj=ProctorAssignment.objects.get(user_id=pk)
                obj.user=proctor
                obj.Block=Block1
                obj.save()
                messages.info(request,'Proctor Block Updated Succesfully...')
                if pr_block !=block1:
                    sched=schedule.objects.all()
                    if len(sched)>0:
                        start_date=str(sched[0].date)
                        n=len(sched)
                        end_date=str(sched[n-1].date)
                        no_shifts=sched[0].num_shift_per_day
                        obj1=schedule.objects.all()
                        obj1.delete()
                        block=Block.objects.all()
                        for i in block:
                            if ProctorAssignment.objects.filter(Block_id=i.id).exists():
                                proctor=ProctorAssignment.objects.filter(Block_id=i.id)
                                lst=[]
                                for i in proctor:
                                    lst.append(i.user_id)
                                generate_schedule(lst,start_date,end_date,no_shifts)
                return redirect('proctor_info')
        else:
            messages.info(request,'User Gender and the Block Purpose does not Match!...')
    setting=settings()
    context={**context,**setting}
        #     return redirect('assign_block')
    return render(request,"Supervisor/update_ProctorAssignment.html",context)
def delete_Proctor_block(request,pk):
    pr=ProctorAssignment.objects.get(user_id=int(pk))
    blk=pr.Block
    sched=schedule.objects.all()
    if len(sched)>0:
        start_date=str(sched[0].date)
        n=len(sched)
        end_date=str(sched[n-1].date)
        no_shifts=sched[0].num_shift_per_day
        for i in sched:
            ptr=ProctorAssignment.objects.get(user=i.procotor)
            if blk==ptr.Block:
                dlsd=schedule.objects.get(id=i.id)
                dlsd.delete()
        pr.delete()
        proctor=ProctorAssignment.objects.filter(Block=blk) 
        lst=[]
        for i in proctor:
            lst.append(i.user_id)
        generate_schedule(lst,start_date,end_date,no_shifts) 
    else:     
        pr.delete()
    messages.error(request,"Proctor Deleted Succesfully!")
    return redirect("proctor_info")
def logout_View(request):
    logout(request)
    #del request.session['username']
    return redirect('index')


from django.db.models import Q
from django.http import JsonResponse

@login_required
def home1(request):
    if 'username' in request.session:
        username = request.session['username']
        users = UserAccount.objects.filter(Role__in=[2, 4])
        chats = {}
        count = 0
        
        # Get all chat messages for the current user
        all_chats = ChatMessage.objects.filter(Q(sender=request.user.id) | Q(reciever=request.user.id))
        for chat in all_chats:
            # Check if the chat message is for the current user and is unseen
            if chat.reciever == request.user and not chat.is_seen:
                count += 1
            # Update the chat message to seen if it is for the current user
            if chat.reciever == request.user:
                chat.is_seen = True
                chat.save()
        if request.method == "POST":
            searched = request.POST.get('search', '')
            AllStudent = []
            if searched:
                # Filter users by role and search query
                users = UserAccount.objects.filter(Role__in=[2, 4], username__icontains=searched).exclude(username=username)
                AllStudent = list(users)
            context = {"AllStudent": AllStudent}
            return render(request, 'Supervisor/home1.html', context)
        
        if request.method == 'GET' and 'u' in request.GET:
            # Get all chat messages between the current user and the other user
            chats = ChatMessage.objects.filter(Q(sender=request.user.id, reciever=request.GET['u']) | Q(sender=request.GET['u'], reciever=request.user.id))
            chats = chats.order_by('timestamp')
            # Update all chat messages from the other user to seen
            for chat in chats.filter(reciever=request.user, is_seen=False):
                chat.is_seen = True
                chat.save()
        # if count==0:
        #     count=str('')
        # else:
        #     count=str(count)
      
        context = {
            "page": "home",
            "users": users,
            "chats": chats,
            "count": count,
            "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
        }
    return render(request, "Supervisor/home1.html", context)

def get_messages(request):
    if 'username' in request.session:
        if request.method == 'POST':
            # Get the last ID of the chat message received by the client
            last_id = request.POST.get('last_id', 0)
            # Get the ID of the chat partner
            chat_id = request.POST.get('chat_id', 0)
            # Get all chat messages between the current user and the chat partner
            chats = ChatMessage.objects.filter(
                Q(id__gt=last_id),
                Q(sender=request.user, reciever=chat_id) | Q(sender=chat_id, reciever=request.user)
            ).order_by('timestamp')
            # Get the username of the current user
            username = request.session.get('username', '')
            # Update the is_seen field of chat messages to mark them as seen
            ChatMessage.objects.filter(reciever=request.user, is_seen=False).update(is_seen=True)
            # Create a list of dictionaries representing the new chat messages
            new_msgs = [{
                'id': chat.id,
                'user_from': chat.sender.id,
                'user_to': chat.reciever.id,
                'message': chat.message,
                'date_created': chat.timestamp.strftime("%b-%d-%Y %H:%M")
            } for chat in chats]
            # Return the new chat messages as a JSON response
            return JsonResponse(new_msgs, safe=False)
        else:
            return JsonResponse([], safe=False)

def send_chat(request):
    if 'username' in request.session:
        resp = {}
        # User = UserAccount()
        if request.method == 'POST':
            post =request.POST
            
            u_from = UserAccount.objects.get(id=post['user_from'])
            u_to = UserAccount.objects.get(id=post['user_to'])
            insert = ChatMessage(sender=u_from,reciever=u_to,message=post['message'],is_seen=False)
            try:
                insert.save()
                resp['status'] = 'success'
            except Exception as ex:
                resp['status'] = 'failed'
                resp['mesg'] = ex
        else:
            resp['status'] = 'failed'

        return HttpResponse(json.dumps(resp), content_type="application/json")