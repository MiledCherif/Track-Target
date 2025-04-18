from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from .models import Profile 
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import Group


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileUpdateForm



from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Friend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .forms import RegisterUserForm
from .models import Profile, Friend
from django.contrib.auth.decorators import login_required


@login_required
def users_list(request):
    current_user = request.user
    query = request.GET.get('q')
    users = User.objects.exclude(id=current_user.id).all()
    if query:
        users = users.filter(username__icontains=query)
    return render(request, 'users_list.html', {'users': users})





@login_required
def friends_list(request):
    profile = request.user.profile
    friends = profile.friends.all()
    query = request.GET.get('q')
    if query:
        friends = friends.filter(username__icontains=query)
    return render(request, 'friends_list.html', {'friends': friends})


@login_required
def add_friend(request, selected_user_id):
    selected_user = get_object_or_404(User, pk=selected_user_id)
    request.user.profile.friends.add(selected_user)
    selected_user.profile.friends.add(request.user)
    return redirect('friends_list')

@login_required
def delete_friend(request, selected_user_id):
    selected_user = get_object_or_404(User, pk=selected_user_id)
    request.user.profile.friends.remove(selected_user)
    selected_user.profile.friends.remove(request.user)
    return redirect('friends_list')



    








def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.save()
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'settings.html', {'profile_form': profile_form})




def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.success(request, ("There Was An Error Loging In, Try Again !!"))
            return redirect('login')
    else:
        return render(request, 'authentication/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logged Out !"))
    return redirect('login')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Inscription Enregistré ! "))

            # Récupérer l'image de profil soumise dans la demande
            profile_image = request.FILES.get('profile_image')

            # Créer une instance de Profile en utilisant les données du formulaire et l'image de profil
            profile = Profile.objects.create(user=user, profile_image=profile_image)

            # Sauvegarder l'instance de Profile
            profile.save()

            # Récupérer le rôle de l'utilisateur créé
            role = form.cleaned_data['role']

            # Assigner l'utilisateur créé au groupe correspondant au rôle
            if role == 'Responsable Commerciale':
                group = Group.objects.get(name='Responsable Commerciale')
                group.user_set.add(user)
                group.save()
            elif role == 'Responsable Marketing':
                group = Group.objects.get(name='Responsable Marketing')
                group.user_set.add(user)
                group.save()
            elif role == 'Administrateur':
                group = Group.objects.get(name='Administrateur')
                group.user_set.add(user)
                group.save()

            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'authentication/register_user.html', {'form':form,})



def settings(request):
    return render(request, 'settings.html', {})
