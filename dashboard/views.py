from django.shortcuts import render, redirect, get_object_or_404
from dashboard.forms import LoginForm, AdminProfileForm, UserForm, AdminProfileForm1
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import AdminProfile


def login_decorator(func):
    return login_required(func, login_url='login')


def logIn(request):
    if request.POST:
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, password=password, username=username)
            if user is not None:
                try:
                    if user.admin_profile.is_admin:
                        login(request, user)
                        messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')
                        return redirect('dashboard')
                except:
                    messages.warning(request, f'Kechirasiz siz admin emas siz!')
                    return redirect("login")
            else:
                messages.warning(request, f'Username yoki parol xato')
        else:
            messages.warning(request, f'Forma noto\'g\'ri to\'ldirilgan')
    else:
        forms = LoginForm()

    return render(request, 'admins/admin/login.html', {'forms': forms})


@login_decorator
def logOut(request):
    logout(request)
    return redirect("login")


@login_decorator
def admin_profile_view(request):
    if request.user.admin_profile.is_admin:
        admin_profile, __ = AdminProfile.objects.get_or_create(user=request.user)
        if request.method == 'POST':
            form = AdminProfileForm(request.POST, request.FILES, instance=admin_profile)
            if form.is_valid():
                admin_profile = form.save()
                admin_profile.user.first_name = form.cleaned_data.get('first_name')
                admin_profile.user.last_name = form.cleaned_data.get('last_name')
                admin_profile.user.email = form.cleaned_data.get('email')
                admin_profile.user.save()

                messages.success(request, 'Profil muvaffaqiyatli saqlandi')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            print(form.errors)
            return redirect('admin_profile')
        
        context = {
            'admin_profile': admin_profile,
            'segment': 'admin_profile',
        }
        return render(request, 'admins/admin/profile.html', context)
    else:
        messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
        return redirect('login')


@login_decorator
def dashboard(request):
    return render(request, 'admins/index.html')


@login_decorator
def admins(request):
    profiles = AdminProfile.objects.all()
    return render(request, 'admins/admin/admins.html', {'profiles': profiles})


@login_decorator
def admins_input(request):
    if request.method == 'POST':
        forms = AdminProfileForm1(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('admins')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
    else:
        forms = AdminProfileForm1()
    return render(request, 'admins/admin/admins_input.html', {'forms': forms})


@login_decorator
def admins_edit(request, pk):
    profile = get_object_or_404(AdminProfile, pk=pk)
    if request.method == 'POST':
        forms = AdminProfileForm1(request.POST, request.FILES, instance=profile)
        if forms.is_valid():
            forms.save()
            return redirect('admins')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
    else:
        forms = AdminProfileForm1(instance=profile)
    return render(request, 'admins/admin/admins_input.html', {'forms': forms})


def create_admin(request):
    if request.method == 'POST':
        forms = UserForm(request.POST)
        print(forms.errors)
        if forms.is_valid():
            print(forms.errors)
            forms.save()
            return redirect('admins_input')  # Success sahifasiga yo'naltiriladi
    else:
        forms = UserForm()
        print(forms.errors)
    return render(request, 'admins/admin/create_admin.html', {'forms':forms})
