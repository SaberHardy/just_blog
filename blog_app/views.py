from django.shortcuts import render


def index(request):
    return render(request, 'blog_app/index.html')
