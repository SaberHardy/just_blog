from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='post-list'),
    path('post/<id>/', views.post, name='post-detail'),
]
