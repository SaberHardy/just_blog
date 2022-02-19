from django.shortcuts import render

from blog_app.models import Post


def index(request):
    queryset = Post.objects.filter(featured=True)
    context = {
        'object_list': queryset
    }
    return render(request, 'blog_app/index.html', context=context)


def post(request):
    return render(request, 'blog_app/post.html')


def blog(request):
    return render(request, 'blog_app/blog.html')
