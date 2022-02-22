from django.shortcuts import render
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from members.forms import UserSignUpForm


class UserRegisterView(generic.CreateView):
    form_class = UserSignUpForm
    template_name = 'registration/registrations.html'
    success_url = reverse_lazy('login')
