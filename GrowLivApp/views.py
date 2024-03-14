# GrowLivApp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser, Business
from .forms import SignUpForm, LoginForm

# GrowLivApp/views.py
from django.shortcuts import render, redirect
# GrowLivApp/views.py
from django.contrib.auth.hashers import make_password
from .models import Photo
from django.shortcuts import render, redirect
from .forms import PhotoForm

def upload_photos(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_images = form.cleaned_data['photo']
            for image in uploaded_images:
                user = CustomUser.objects.filter(username=request.user)
                Photo.objects.create(user=user[0], image=image)
            return redirect('GrowLivApp:home')  # Redirect to your home or another page after successful upload
    else:
        form = PhotoForm()

    return render(request, 'GrowLivApp/upload_photos.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = CustomUser(username=username, email=email, password=make_password(password))
            user.save()

            # Redirect to login or home page
            return redirect('GrowLivApp:login')
    else:
        form = SignUpForm()

    return render(request, 'GrowLivApp/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = CustomUser.objects.get(username=username)
                if check_password(password, user.password):
                    # Set session variables
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username

                    return redirect('GrowLivApp:home')
                else:
                    # Incorrect password
                    return render(request, 'GrowLivApp/login.html', {'form': form, 'error': 'Invalid credentials'})
            except CustomUser.DoesNotExist:
                # User does not exist
                return render(request, 'GrowLivApp/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()

    return render(request, 'GrowLivApp/login.html', {'form': form})

def home(request):
    # Retrieve user information from session
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    return render(request, 'GrowLivApp/home.html', {'username': username})
