import uuid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse

# Create your views here.
from App_auth.forms import *
from App_auth.models import ProfileModel


def login_or_signup(request):
    return render(request, 'App_auth/login_or_signup.html')


def login_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('App_main:home'))
        else:
            createUser = User(username=email)
            createUser.set_password(password)
            createUser.save()
            user = authenticate(username=email, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('App_main:home'))

    return HttpResponseRedirect(reverse('App_auth:login-signup'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_auth:login-or-signup'))


def profile_view(request):
    if not ProfileModel.objects.filter(user=request.user).exists():
        return HttpResponseRedirect(reverse('App_auth:profile-submit'))
    profilePictureForm = ProfilePictureForm()
    yourProfile = ProfileModel.objects.get(user=request.user)
    content = {
        'profilePictureForm': profilePictureForm,
        'profile': yourProfile
    }
    return render(request, 'App_auth/profileView.html', context=content)


def profile_submit(request):
    form = ProfileModelForm()
    if request.method == 'POST':
        photo = request.FILES.get('photoFile')
        form = ProfileModelForm(request.POST, request.FILES)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.user = request.user
            payment_id = uuid.uuid4()
            if photo is None:
                pass
            else:
                thisForm.profile_picture = photo
            thisForm.paymentID = payment_id
            thisForm.save()
            return HttpResponseRedirect(reverse('App_auth:profile-view'))
    content = {
        'form': form,
    }

    return render(request, 'App_auth/profileSubmit.html', context=content)


def profile_picture_upload(request):
    if request.method == 'POST':
        profilePicture = request.FILES.get('photoFile')
        profile = ProfileModel.objects.get(user=request.user)
        profile.profile_picture = profilePicture
        profile.save()
        return HttpResponseRedirect(reverse('App_auth:profile-view'))

    return HttpResponseRedirect(reverse('App_auth:profile-view'))
