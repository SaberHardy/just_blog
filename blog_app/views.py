from django.shortcuts import render

from blog_app.models import Post


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[:3]
    context = {
        'object_list': featured,
        'latest': latest,
    }
    return render(request, 'blog_app/index.html', context=context)


def post(request):
    return render(request, 'blog_app/post.html')


def blog(request):
    return render(request, 'blog_app/blog.html')
