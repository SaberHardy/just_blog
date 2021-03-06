from django.contrib.auth import login as auth_login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from blog_app.forms import CommentForm, PostForm
from blog_app.models import Post, Author, PostView
from marketing.models import Signup


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(Q(title__icontains=query) |
                                   Q(overview__icontains=query)).distinct()

    context = {
        'queryset': queryset,
    }
    return render(request, 'blog_app/search_results.html', context)


def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset


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


def post(request, id):
    post = get_object_or_404(Post, id=id)
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)


    form = CommentForm(request.POST or None)
    print(f"The user is id-{request.user}")

    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail', kwargs={'id': post.id}))
    context = {
        'post': post,
        'category_count': category_count,
        'most_recent': most_recent,
        'form': form,
    }
    return render(request, 'blog_app/post.html', context)


def blog(request):
    category_count = get_category_count()
    post_list = Post.objects.all()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    paginator = Paginator(post_list, per_page=4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
    }
    return render(request, 'blog_app/blog.html', context=context)


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)

    print(f"the user is: {request.user}")
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'blog_app/create_post.html', context)


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,
                    request.FILES or None,
                    instance=post)

    author = get_author(request.user)

    print(f"the user is: {request.user}")
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'blog_app/create_post.html', context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('post-list')


"""
This is for render matplotlib images after plotting
from django.shortcuts import render
import matplotlib.pyplot as plt
import base64
import urllib
import io


def index(request):
    if request.method == "POST":
        cat = list(request.POST['xaxis'].split(','))
        dog = list(request.POST['yaxis'].split(','))
        activity = list(request.POST['activity'].split(','))

        fig, ax = plt.subplots()
        ax.plot(activity, dog, label="dog")
        ax.plot(activity, cat, label="cat")
        ax.legend()

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        uri = 'data:image/png;base64,' + urllib.parse.quote(string)

        context = {'image': uri}

        return render(request, 'index.html', context=context)
    else:
        return render(request, 'index.html')


In Template use this

{% if image %}
    <img src="{{ image }}">
{% endif %}

"""
