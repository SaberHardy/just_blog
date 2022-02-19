from django.shortcuts import render


def index(request):
    return render(request, 'blog_app/index.html')


def post(request):
    return render(request, 'blog_app/post.html')


def blog(request):
    return render(request, 'blog_app/blog.html')
