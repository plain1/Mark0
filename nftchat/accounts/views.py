from django.shortcuts import render, redirect
from django.contrib import auth
from .models import User 
 
def signup(request):
      if request.method == "POST":
            if request.POST["password"] == request.POST["password2"]:
                  user = User.objects.create_user(
                        username=request.POST["username"],
                        password=request.POST["password"],
                        name = request.POST['name'],
                        birth = request.POST['birth'],
                        gender = request.POST['gender'],
                        phone = request.POST['phone'],
                        digitalwallet = request.POST['digitalwallet'],
                        nftwallet = request.POST['nftwallet']
                  )
                  auth.login(request,user)
                  return render(request, 'login.html')
            return render(request, 'signup.html')
      return render(request,'signup.html')

def login(request):
    if request.method == 'POST' : 
      username = request.POST['username']
      password = request.POST['password']
      user = auth.authenticate(request, username=username, password=password)
       
      if user is not None:
            auth.login(request,user)
            return redirect('main')
      else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})	
    else: 
         return render(request,'login.html')      

def logout(request):
    auth.logout(request)
    return redirect('')

