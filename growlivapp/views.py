from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import PhotoForm
from .forms import SignUpForm, LoginForm
from .models import Photo


def upload_photos(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_images = form.cleaned_data['photo']
            for image in uploaded_images:
                user = User.objects.get(username=request.user)
                Photo.objects.create(user=user, image=image)
            return redirect('growlivapp:home')  # Redirect to your home or another page after successful upload
    else:
        form = PhotoForm()

    return render(request, 'growlivapp/upload_photos.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User(username=username, email=email, password=make_password(password))
            user.save()

            # Redirect to login or home page
            return redirect('growlivapp:login')
    else:
        form = SignUpForm()

    return render(request, 'growlivapp/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    # Set session variables
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username

                    return redirect('growlivapp:home')
                else:
                    # Incorrect password
                    return render(request, 'growlivapp/login.html', {'form': form, 'error': 'Invalid credentials'})
            except User.DoesNotExist:
                # User does not exist
                return render(request, 'growlivapp/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()

    return render(request, 'growlivapp/login.html', {'form': form})


def Instructions(request):
    return render(request, 'GrowLivApp/instruction.html')


def profile(request):
    return render(request, 'GrowLivApp/profile.html')


def history(request):
    return render(request, 'GrowLivApp/scan_details.html')


def home(request):
    # Retrieve user information from session
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    return render(request, 'growlivapp/home.html', {'username': username})
