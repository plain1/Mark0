from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from main.models import FriendRequest, FriendList
from django.contrib.auth.decorators import login_required
import json
from chat.models import Room
from accounts.models import User
from mint.views import mint

@login_required(login_url='')
def main(request):
    return render(request, 'main.html')

@login_required(login_url='')
def profiles(request):
    if request.method == 'POST':
        user = User.objects.all(
            username=request.GET["username"],
            password=request.GET["password"],
            name = request.GET['name'],
            birth = request.GET['birth'],
            gender = request.GET['gender'],
            phone = request.GET['phone'],
            digitalwallet = request.GET['digitalwallet'],
            nftwallet = request.GET['nftwallet']
        )
        params = {
            user
        }
        print(params)
    return render(request,'profiles.html')

@login_required(login_url='')
def friendlists(request, *args, **kwargs):
    context = {}
    user = request.user
    user_id = kwargs.get('user_id')
    if user_id:
        try:
            accounts = User.objects.get(pk=user_id)
            context = {
                'accounts': accounts
                }
        except User.DoesNotExist:
            return render(request, 'main.html')

        try:
            friendslist = FriendList.objects.get(user=accounts)

        except FriendList.DoesNotExist:
            pass

        #must be friends to view friend list
        if user != accounts:
            if not user in friendslist.friends.all():
                return render(request, 'main.html')

        friends = [] #[(account, false), (account, True)]
        auth_user_friend_list = FriendList.objects.get(user=user)
        for friend in friendslist.friends.all():
            friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))

        context['friends'] = friends
        context['username'] = accounts.username
    else:
        return render(request, '')

    return render(request, 'friendlists.html', context)

@login_required(login_url='')
def friend_requests(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get('user_id')
        try:
            account = User.objects.get(pk=user_id)


            if user == account:
                friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
                context = {
                  'friend_requests': friend_requests
                }
            else:
                return render(request, 'main.html')

        except User.DoesNotExist:
            pass
    else:
        return redirect('login.html')
    return render(request, 'friend_requests.html', context)

@login_required(login_url='')
def send_friend_request(request, *args, **kwargs):
    sender = request.user
    payload = {}
    if request.method == "POST" and request.user.is_authenticated:

        user_id = request.POST.get('receiver_id')
        if user_id:
            receiver = User.objects.get(pk=user_id)

            try:
                #get all the friend requests
                print("check friend requests")
                friend_requests = FriendRequest.objects.filter(sender=sender, receiver=receiver)

                #find if any one is active
                for request in friend_requests:
                    print("loop")
                    if request.is_active:
                        print("active")
                        #if there is already an active request
                        payload['response'] = "error"


                #if none are active, then sent a request
                friend_request = FriendRequest(sender=sender, receiver=receiver)
                friend_request.save()
                payload['response'] = "success"


            #if none are active, then sent a request
            except FriendRequest.DoesNotExist:
                print("check friend requests2")
                friend_request = FriendRequest(sender=sender, receiver=receiver)
                friend_request.save()
                payload['response'] = "success"

            if payload['response'] == None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Something went wrong."
    else:
        payload['response'] = "You have to login to sent a friend request."

    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='')
def cancel_friend_request(request, *args, **kwargs ):
    sender = request.user
    payload = {}
    if request.method == "POST" and request.user.is_authenticated:
        receiver_id = request.POST.get('receiver_id')
        if receiver_id:
            receiver = User.objects.get(pk=receiver_id)
            try:
                friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver, is_active = True)

                friend_request.cancel()
                payload['response'] = 'deleted'
            except FriendRequest.DoesNotExists:
                payload['response'] = 'error'
        else:
            payload['response'] = 'error'
    else:
        payload['response'] = 'error'

    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='')
def decline_friend_request(request, *args, **kwargs):
    receiver = request.user
    payload = {}
    if request.method == "POST" and request.user.is_authenticated:

        request_id = request.POST.get('friend_request_id')
        if request_id:

            try:
                friend_request = FriendRequest.objects.get(pk=request_id)
                if friend_request.receiver == receiver:
                    friend_request.decline()
                    payload['response'] = 'declined'
                else:
                    payload['response'] = 'error'

            except FriendRequest.DoesNotExists:
                payload['response'] = 'error'
        else:
            payload['response'] = 'error'
    else:
        payload['response'] = 'error'
    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='')
def confirm_friend_request(request, *args, **kwargs):
    receiver = request.user
    payload = {}
    if request.method == "POST" and request.user.is_authenticated:
        request_id = request.POST.get('friend_request_id')
        if request_id:
            try:
                friend_request = FriendRequest.objects.get(pk=request_id)
                if friend_request.receiver == receiver:
                    friend_request.accept()
                    payload['response'] = 'confirmed'

            except FriendRequest.DoesNotExist:
                payload['response'] = 'error'
        else:
            payload['response'] = 'error'

    else:
        payload['response'] = 'error'

    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required(login_url='')
def unfriend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        print(user_id)
        if user_id:
            try:
                remove = User.objects.get(pk=user_id)  
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(remove)
                payload['response'] = "Successfully removed that friend."
            except User.DoesNotExist:

                payload['response'] = f"Something went wrong: {str(e)}"
        else:
            payload['response'] = 'There was an error. Unable to remove that friend'
    else:

        payload['response'] = "You must be authenticated to remove a friend."
    return HttpResponse(json.dumps(payload), content_type="application/json")

#채팅목록보여주기
@login_required(login_url='')
def chatlists(request):
    chatlists=Room.objects.filter(users=request.user,type=0)
    return render(request,'chatlists.html', chatlists)


@login_required(login_url='')
def market(request):
    return render(request,"market.html")
