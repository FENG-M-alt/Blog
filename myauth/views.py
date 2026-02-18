from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as lg
from django.contrib.auth import logout as lt


User = get_user_model()
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                lg(request, user)
                # 判断是否记住
                if not remember:
                    # 如果没有设置记住我，则关闭浏览器后即删除
                    request.session.set_expiry(0)
                return redirect("/")
            else:
                print("邮箱或密码错误！")
                return redirect(reverse('myauth:login'))

def logout(request):
    lt(request)
    return redirect('/')

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('myauth:login'))
        else:
            print(form.errors)
            # 重新挑战到注册页面
            return redirect(reverse('myauth:register'))

def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400,"message": "必须传递邮箱"})
    # 随机四位数字作为验证码
    captcha = "".join(random.sample(string.digits, 4))
    # 存储或者更新验证码信息
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail("博客注册验证码", message=f"您的注册验证码为：{captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({"code": 200,"message": "邮箱验证码发送成功"})