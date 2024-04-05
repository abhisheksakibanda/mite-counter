from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from counterapp.models import Result
from .forms import VideoForm, BusinessForm, ForgotPasswordForm
from .models import Business


def scan_detail_page(request):
    # Fetch all scan results or use filters as needed
    scan_results = Result.objects.filter(video__business__email=request.user.email).order_by('-scan_date')

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

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.username = form.cleaned_data.get('email')
            form.save()
            return HttpResponseRedirect(redirect_to=reverse(viewname='growlivapp:login'))
        return render(request, template_name='growlivapp/signup.html', context={'form': form})


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
    if request.method == 'POST':
        form = BusinessForm(request.POST, instance=business)
        business.email = form.data.get('email')
        business.username = form.data.get('email')
        business.business_name = form.data.get('business_name')
        business.business_phone = form.data.get('business_phone')
        business.contact_person_name = form.data.get('contact_person_name')
        business.save()
        return redirect('growlivapp:profile')
    else:
        form = BusinessForm(instance=business)
    return render(request, template_name='growlivapp/profile.html', context={'business': form})


def forgot_password(request):
    forget_pswd_form = ForgotPasswordForm()
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            return render(request, template_name='growlivapp/instruction.html')
        except User.DoesNotExist:
            return render(request, template_name='growlivapp/forgot_password.html',
                          context={'err': 'The email you entered does not exist in our records.',
                                   'form': forget_pswd_form})
    return render(request, template_name='growlivapp/forgot_password.html', context={'form': forget_pswd_form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('growlivapp:profile')
        else:
            # If form is not valid, add a generic message or specific error messages
            messages.error(request, 'Please correct the errors below.')
            # Optionally, add specific form error messages
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'growlivapp/changepassword.html', {'form': form})


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


def delete_record(request, record_id: int) -> HttpResponseRedirect:
    video = Result.objects.get(id=record_id)
    video.delete()
    return redirect('growlivapp:scan_detail_page')
