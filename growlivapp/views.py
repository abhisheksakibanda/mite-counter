from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from counterapp.models import Result
from .forms import VideoForm, BusinessForm
from .models import Business


def scan_detail_page(request):
    # Fetch all scan results or use filters as needed
    scan_results = Result.objects.all().order_by('-scan_date')

    # Pass the results to the template
    context = {
        'scan_results': scan_results,
    }
    return render(request, template_name='growlivapp/scan_details.html', context=context)


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            business = Business.objects.get(username=request.user)
            video = form.save(commit=False)
            video.business = business
            video.save()
            return redirect('counterapp:predict', video_id=video.id)

    else:
        form = VideoForm()

    return render(request, template_name='growlivapp/home.html', context={'form': form})


class BusinessRegisterView(CreateView):
    template_name = 'growlivapp/signup.html'
    form_class = BusinessForm
    success_url = reverse_lazy('growlivapp:login')

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=reverse(viewname='growlivapp:home'))
        return super().get(request=request, *args, **kwargs)


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs.update({
            'class': 'un',
            'placeholder': 'Email'
        })
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs.update({
            'class': 'un',
            'placeholder': 'Password'
        })


class BusinessLoginView(LoginView):
    template_name = 'growlivapp/login.html'
    form_class = CustomAuthenticationForm

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect | HttpResponse:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user:
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                login(request=request, user=user)
                return HttpResponseRedirect(redirect_to=reverse(viewname='growlivapp:home'))
            else:
                return render(request, template_name='growlivapp/login.html',
                              context={'err': 'Login details are incorrect. Please try again.',
                                       'form': CustomAuthenticationForm(request.POST)})
        else:
            return render(request, template_name='growlivapp/login.html',
                          context={'err': 'Login details are incorrect. Please try again.',
                                   'form': CustomAuthenticationForm(request.POST)})

    def get(self, request, *args, **kwargs) -> HttpResponseRedirect | HttpResponse:
        if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=reverse(viewname='growlivapp:home'))
        return super().get(request=request, *args, **kwargs)


def instructions(request):
    return render(request, template_name='growlivapp/instruction.html')


def profile(request):
    business = Business.objects.get(email=request.user.email)
    return render(request, template_name='growlivapp/profile.html', context={'business': business})


@login_required
def home(request):
    # Retrieve user information from session
    user_id = request.session.get('user_id')
    username = request.session.get('username')

    return render(request, template_name='growlivapp/home.html', context={'username': username})


@login_required
def logout_user(request) -> HttpResponseRedirect:
    logout(request=request)
    return HttpResponseRedirect(redirect_to=reverse(viewname='growlivapp:login'))
