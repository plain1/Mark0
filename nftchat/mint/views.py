from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import nft_collection
from thirdweb.types.nft import NFTMetadataInput 
from io import BytesIO
from accounts.models import User
from .models import Shopping, Register
from .form import ShoppingForm, RegisterForm
import os
import requests
from dotenv import load_dotenv
from thirdweb import ThirdwebSDK

load_dotenv()

#민팅
@login_required(login_url='')
def mint(request):
    if request.method == 'POST' and request.FILES['home']:
        name_nft = request.POST.get('name','')
        description_nft = request.POST.get('description','')
        image_nft = request.FILES['home'].file
        image_nft.name = request.POST.get('name','')
        prop = {}
 
        nft_metadata = {
            'name': name_nft,
            'description': description_nft,
            'image': image_nft,
            'properties':prop
        }

        print(nft_metadata)
        nft_collection.nft_collection.mint(NFTMetadataInput.from_json(nft_metadata))        
        #sdk = ThirdwebSDK("mumbai")
        #contract = sdk.get_contract("0xFF1362E47355FC3d21ba383E501474eB7c40BfC4") 
        #_tokenId = contract.call("nextTokenIdToMint") - 1 
        #data = contract.call("tokenURI", _tokenId)
        #name = contract.call("name")
        #register = Register.objects.create(
        #    name = request.post['nft_name'], 
        #    data = request.post['Token_uri'], 
        #    _tokenId = request.post['Token_id'],
        #      
        #    )
        return redirect("register")
    return render(request,'mint.html',{})


#거래
DJANGO_APP_KAKAOPAY_API_ADMIN_KEY = os.environ.get("DJANGO_APP_KAKAOPAY_API_ADMIN_KEY")

@login_required(login_url='')
def register(request):
    if request.method == 'POST':
        register_nft = Register.objects.create(
            room_name=request.POST['room_name'],
            nft_price=request.POST['nft_price'],
        )


        
        return render(request,"chatroom.html")
    return render(request, "register.html")


@login_required(login_url='')
def trade(request):
    if request.method == 'POST': 
        first_form = ShoppingForm(request.POST)
        if first_form.is_valid():
            # 결제 단계 넘어가면 일단, Shopping Table에 데이터 추가(대신, 구매 확정은 False)
            form = first_form.save(commit=False)
            form.total_amount = int(form.item_price)
            form.save()

            URL = 'https://kapi.kakao.com/v1/payment/ready'
            headers = {
                "Authorization": "KakaoAK " + DJANGO_APP_KAKAOPAY_API_ADMIN_KEY,
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            }
            params = {
                "cid": "TC0ONETIME",    # 테스트용 제휴코드
                "partner_order_id": form.id,     # 주문번호
                "partner_user_id": form.customer_name,    # 유저 아이디
                "nft_name": form.nft_name,        # 구매 물품 이름
                "nft_price": form.nft_price,        # 구매 물품 가격
                "approval_url": "http://127.0.0.1:8000/approval",
                "cancel_url": "http://127.0.0.1:8000/market",
                "fail_url": "http://127.0.0.1:8000/market",
            }
            response = requests.post(URL, headers=headers, params=params)

            request.session['tid'] = response.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
            request.session['order_id'] = form.id      # 결제 승인시 사용할 order_id를 세션에 저장
            request.session['customer_name'] = form.customer_name      # 결제 승인시 사용할 customer_name을 세션에 저장
            next_url = response.json()['next_redirect_pc_url']   # 결제 페이지로 넘어갈 url을 저장
            return redirect(next_url)

    if request.method == "GET":
        form = ShoppingForm()
        context = {'form':form}
        return render(request, 'trade.html', context)

@login_required(login_url='')
def approval(request):
    if request.method == 'GET':
        # 결제 승인단계에서 해당 쇼핑을 구매 확정 처리
        order_id = request.session['order_id']
        shopped_history = get_object_or_404(Shopping, pk=order_id)
        shopped_history.is_complete = True
        shopped_history.save()

        URL = 'https://kapi.kakao.com/v1/payment/approve'
        headers = {
                "Authorization": "KakaoAK " + DJANGO_APP_KAKAOPAY_API_ADMIN_KEY,
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
            "partner_order_id": order_id,     # 주문번호
            "partner_user_id": request.session['customer_name'],    # 유저 아이디
            "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
        }
        response = requests.post(URL, headers=headers, params=params)
        amount = response.json()['amount']['total']
        context = {
            'response': response.json(),
            'amount': amount,
        }
        return redirect('transfer')
    return render(request, 'approval.html', context)

@login_required(login_url='')
def history(request):
    histories = Shopping.objects.filter(is_complete=True).order_by("-shopped_date")
    context = {'histories':histories}
    return render(request, 'history.html', context)

@login_required(login_url='')
def transfer(request):
    if request.method == "POST":
        sdk = ThirdwebSDK("mumbai")
        contract = sdk.get_contract("0xFF1362E47355FC3d21ba383E501474eB7c40BfC4")
        wallet = User.objects.get(nftwallet="nftwallet")
        Token_id = Register.objects.get("Token_id")
        to  =  {{wallet}}
        contract.transfer(to, Token_id)
        return redirect('market')
    return render('transfer.html')