from django.shortcuts import render,redirect
from django.contrib import auth
from .models import CustomUser
from django.core.cache import cache
from django.contrib.auth.models import User
# redis
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
# password encrypt
import bcrypt
salt = bcrypt.gensalt()
# import rsa
# pub_key,priv_key = rsa.newkeys(512)

def login_page(request):
    user = User.objects.create_user("username", "password")
    return render(request,'accounts/login.html')

def user_login(request):
    custom_user = CustomUser()
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        # user auth
        if CustomUser.objects.filter(username=username).exists():
            check_id=CustomUser.objects.get(username=username)
            # if bcrypt.checkpw(password, check_id.password)==True: # 비밀번호 인증법 추가 : 지속적 오류 발생
            r.set(f'{username}',password)
            return redirect("crud:index")
            # else:
            #     print("로그인 정보가 잘못됐습니다.")
            #     return render(request,'accounts/login.html')
        else:
            print("회원정보가 존재하지 않습니다.")
            return render(request,'accounts/login.html')    
    else:
        return render(request,'accounts/login.html')

def signup(request):
    custom_user = CustomUser()
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password").encode('utf-8')
        hashed_password = bcrypt.hashpw(password, salt)
        custom_user.username=username
        custom_user.password=hashed_password
        if CustomUser.objects.filter(username=username).exists(): # 아이디 중복 방지
            print("존재하는 아이디입니다.")
            return render(request,'accounts/signup.html')
        else:
            custom_user.save()
        return redirect("crud:index")
    else:
        return render(request,'accounts/signup.html')

def logout(request):
    r.flushall() # 모든 값을 지운다.
    return redirect("crud:index")