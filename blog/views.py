from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import BlogCategory, Blog, BlogComment
from .forms import PubBlogForm
from django.db.models import Q
import os
from datetime import datetime
from django.conf import settings
# Create your views here.

def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', context={'blogs':blogs})

def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog=None
    return render(request,'blog_detail.html', context={'blog': blog})

@require_http_methods(['GET', 'POST'])
# 在urls.py加载在内存后再去作路由反转
@login_required(login_url=reverse_lazy('myauth:login'))
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context = {'categories': categories})
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({'code': 200, 'message': '博客发布成功！', "data": {"blog_id": blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code': 400, 'message': '参数错误！'})

@require_POST
@login_required(login_url=reverse_lazy('myauth:login'))
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    content = request.POST.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    return redirect(reverse("blog:blog_detail", kwargs={'blog_id': blog_id}))

@require_GET
def search(request):
    q = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return render(request, 'index.html', context={'blogs':blogs})


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        folder = 'uploads'
        save_dir = os.path.join(settings.MEDIA_ROOT, folder)
        os.makedirs(save_dir, exist_ok=True)

        filename = datetime.now().strftime('%Y%m%d%H%M%S%f') + os.path.splitext(file.name)[-1]
        file_path = os.path.join(save_dir, filename)

        with open(file_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        url = request.build_absolute_uri(f'/media/{folder}/{filename}')
        return JsonResponse({
            'errno': 0,
            'data': { 'url': url }
        })

    return JsonResponse({'errno': 1})


def upload_video(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        folder = 'uploads'
        save_dir = os.path.join(settings.MEDIA_ROOT, folder)
        os.makedirs(save_dir, exist_ok=True)

        filename = datetime.now().strftime('%Y%m%d%H%M%S%f') + os.path.splitext(file.name)[-1]
        file_path = os.path.join(save_dir, filename)

        with open(file_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        url = request.build_absolute_uri(f'/media/{folder}/{filename}')
        return JsonResponse({
            'errno': 0,
            'data': { 'url': url }
        })

    return JsonResponse({'errno': 1})