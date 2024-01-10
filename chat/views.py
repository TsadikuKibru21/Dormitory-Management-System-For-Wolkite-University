from django.shortcuts import render, HttpResponse, redirect
from .models import Messages
from account.models import Role, UserAccount
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer


def getFriendsList(id):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """
    try:
        user = UserAccount.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = UserAccount.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []


def getUserId(username):
    """
    Get the user id by the username
    :param username:
    :return: int
    """
    use = UserAccount.objects.get(username=username)
    id = use.id
    return id


def chatindex(request):
    """
    Return the home page
    :param request:
    :return:
    """
    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        username = request.user.username
        id = getUserId(username)
        friends = getFriendsList(id)
        return render(request, "chat/Base.html", {'friends': friends})


def search(request):
    """
    Search users page
    :param request:
    :return:
    """
    # student_dean=Role.objects.get(R_name='Student_Dean')
                  
    #                 # Filter users by role and search query
    #                 users = UserAccount.objects.filter(Role__in=[student_dean], 
    username=request.user.username
    acc=UserAccount.objects.get(username=username)
    role_id=acc.Role_id
    rr=Role.objects.get(id=role_id)
    users=[]
    if rr.R_name=="Student_Dean":
        president=Role.objects.get(R_name='President')
        registrar=Role.objects.get(R_name='Registrar')
        admin=Role.objects.get(R_name='Admin')
        supervisor=Role.objects.get(R_name='Supervisor')
        users = list(UserAccount.objects.filter(Role__in=[president,registrar,admin,supervisor]))
    elif rr.R_name=="Supervisor":
        studendean=Role.objects.get(R_name='Student_Dean')
        proctor=Role.objects.get(R_name='Proctor')
        users = list(UserAccount.objects.filter(Role__in=[studendean,proctor]))
    elif rr.R_name=="Registrar":
        studendean=Role.objects.get(R_name='Student_Dean')
        users = list(UserAccount.objects.filter(Role__in=[studendean]))
    elif rr.R_name=="Proctor":
        supervisor=Role.objects.get(R_name='Supervisor')
        users = list(UserAccount.objects.filter(Role__in=[supervisor]))
    elif rr.R_name=="President":
        studendean=Role.objects.get(R_name='Student_Dean')
        users = list(UserAccount.objects.filter(Role__in=[studendean]))
    elif rr.R_name=="Admin":
        studendean=Role.objects.get(R_name='Student_Dean')
        users = list(UserAccount.objects.filter(Role__in=[studendean]))
       
    for user in users:
        if user.username == request.user.username:
            users.remove(user)
            break
    try:
        users = users[:10]
    except:
        users = users[:]
    id = getUserId(request.user.username)
    friends = getFriendsList(id)
    if request.method == "POST":
        print("SEARCHING!!")
        query = request.POST.get("search")
        user_ls = []
        for user in users:
            if query in user.username:
                user_ls.append(user)
        return render(request, "chat/search.html", {'users': user_ls, 'friends': friends})

   
    return render(request, "chat/search.html", {'users': users, 'friends': friends})


def addFriend(request, name):
    """
    Add a user to the friend's list
    :param request:
    :param name:
    :return:
    """

    username = request.user.username
    id = getUserId(username)
    friend = UserAccount.objects.get(username=name)
    curr_user = UserAccount.objects.get(id=id)
    
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.id:
            flag = 1
            break
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)
    return redirect("search")


from django.shortcuts import render, HttpResponse

def chat(request, username):
    """
    Get the chat between two users.
    :param request:
    :param username:
    :return:
    """
    friend = UserAccount.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = UserAccount.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)

    if request.method == "GET":
        friends = getFriendsList(id)
        return render(request, "chat/messages.html", {
            'messages': messages,
            'friends': friends,
            'curr_user': curr_user,
            'friend': friend
        })

    # # Handle the default case for the GET request
    # friends = getFriendsList(id)
    # return render(request, "chat/messages.html", {
    #     'messages': messages,
    #     'friends': friends,
    #     'curr_user': curr_user,
    #     'friend': friend
    # })



@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
def backpage(request):
    if 'username' in request.session:
        username=request.session['username']
        user=UserAccount.objects.get(username=username)
        r=user.Role_id
        role=Role.objects.get(id=r)
        role_name=role.R_name
        if role_name=='Student_Dean':
            return redirect('studentdeanhome')
        elif role_name=='Supervisor':
            return redirect('supervisor')
        elif role_name=='Proctor':
            return redirect('proctor')
        elif role_name=='Registrar':
            return redirect('Registrar')
        elif role_name=='President':
            return redirect('President')
        elif role_name=='Admin':
            return redirect('LAdmin')
