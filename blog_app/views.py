from django.shortcuts import render

from blog_app.models import Post
from marketing.models import Signup


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[:3]

    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
    }
    return render(request, 'blog_app/index.html', context=context)


def post(request):
    return render(request, 'blog_app/post.html')


def blog(request):
    post_list = Post.objects.all()
    context = {
        'post_list': post_list
    }
    return render(request, 'blog_app/blog.html', context=context)
