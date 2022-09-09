from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from accounts.models import User
from django.http import HttpResponse
from django.utils import timezone
from thirdweb import ThirdwebSDK

       
#채팅방생성
@login_required(login_url = '')
def chatroom(request, Token_id):
    room = Room.objects.create(
        Token_id = Token_id
        
        )
    return render(request, 'chatroom.html', {
        'Token_id' : Token_id
    })
 
#채팅방검색
def search(request):
    rooms = Room.objects.all()
    q = request.POST.get('q',"")
    if q:
        rooms = rooms.filter(title__icontains=q)
        return redirect('search', {'rooms':rooms, 'q':q})
    return render(request,'search.html')

# 채팅방 입장(nft로 입장가능)
@login_required(login_url = '')
def enter_room(request, Token_id):
    if request.method == "POST":
        sdk = ThirdwebSDK("mumbai")
        contract = sdk.get_contract("0xFF1362E47355FC3d21ba383E501474eB7c40BfC4")
        _tokenId= contract.call("nextTokenIdToMint")-1
        #uri = contract.call('tokenURI', _tokenId)
        data = User.objects.get(nftwallet = "nftwallet")
        Token_id = contract.call("safeTransferFrom", "0xD709db1da17068B4f87F61A7C23b5ef2C9Ff26bF", data, _tokenId)
        if Token_id == True:
            return redirect('makechat/mint/<int:Token_id>')
    return render(request, "chatlists.html")


