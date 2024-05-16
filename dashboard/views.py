from django.shortcuts import render, redirect, get_object_or_404
from dashboard.forms import LoginForm, AdminProfileForm, UserForm, AdminProfileForm1
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import AdminProfile
from carrental.models import Cars, CarRentai, Review
from dashboard.forms import CarsFrom, CarBrendsForm, CarModelsForm, CarYearForm, CarPriceForm, Manzil1Form, Manzil2Form, ReviewForm

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
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
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
                'application':application,
            }
            return render(request, 'admins/admin/profile.html', context)
        else:
            messages.warning(request, 'Sizda admin ruxsati yo\'q. Foydalanuvchi sahifasiga o\'tishingiz mumkin.')
            return redirect('login')
    except:
        messages.warning(request, 'Siz admin emasiz') 


@login_decorator
def dashboard(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            return render(request, 'admins/index.html', {"application":application})
        else:
            messages.warning(request, 'Siz admin emasiz') 
            return render('home')
    except:
        messages.warning(request, 'Siz admin emasiz') 


@login_decorator
def admins(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            profiles = AdminProfile.objects.all()
            return render(request, 'admins/admin/admins.html', {'profiles': profiles, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz') 


@login_decorator
def admins_input(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            if request.method == 'POST':
                forms = AdminProfileForm1(request.POST, request.FILES)
                if forms.is_valid():
                    forms.save()
                    messages.success(request, 'Muvafaqiyatli') 
                    return redirect('admins')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
            else:
                forms = AdminProfileForm1()
            return render(request, 'admins/admin/admins_input.html', {'forms': forms, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz')     


@login_decorator
def admin_delete(request, pk):
    forms = AdminProfile.objects.get(pk=pk)
    forms.delete()
    return redirect('admins') 


@login_decorator
def admins_edit(request, pk):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            profile = get_object_or_404(AdminProfile, pk=pk)
            if request.method == 'POST':
                forms = AdminProfileForm1(request.POST, request.FILES, instance=profile)
                if forms.is_valid():
                    forms.save()
                    return redirect('admins')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
            else:
                forms = AdminProfileForm1(instance=profile)
            return render(request, 'admins/admin/admins_input.html', {'forms': forms, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz')     


@login_decorator
def create_admin(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
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
            return render(request, 'admins/admin/create_admin.html', {'forms':forms, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz')        


@login_decorator
def cars(request):
    application = Review.objects.all().filter(status='yangi')
    cars = Cars.objects.all()
    return render(request, 'admins/mashina/cars.html', {'cars': cars, "application":application})


@login_decorator
def car_input(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            if request.method == 'POST':
                forms = CarsFrom(request.POST, request.FILES)
                if forms.is_valid():
                    forms.save()
                    messages.success(request, 'Muvafaqiyatli') 
                    return redirect('cars')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
            else:
                forms = CarsFrom()
            return render(request, 'admins/mashina/car_input.html', {'forms': forms, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz') 


@login_decorator
def car_delete(request, pk):
    forms = Cars.objects.get(pk=pk)
    forms.delete()
    return redirect('cars') 

@login_decorator
def cars_edit(request, pk):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            car = get_object_or_404(Cars, pk=pk)
            if request.method == 'POST':
                forms = CarsFrom(request.POST, request.FILES, instance=car)
                if forms.is_valid():
                    forms.save()
                    return redirect('cars')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
            else:
                forms = CarsFrom(instance=car)
            return render(request, 'admins/mashina/car_input.html', {'forms': forms, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz')  

@login_decorator
def carmodels_input(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            if request.method == 'POST':
                forms = CarModelsForm(request.POST, request.FILES)
                if forms.is_valid():
                    forms.save()
                    messages.success(request, 'Muvafaqiyatli') 
                    return redirect('cars')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
            else:
                forms = CarModelsForm()
            return render(request, 'admins/mashina/carmodels_input.html', {'forms': forms, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz') 

@login_decorator
def carbreand_input(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            if request.method == 'POST':
                forms = CarBrendsForm(request.POST, request.FILES)
                if forms.is_valid():
                    forms.save()
                    messages.success(request, 'Muvafaqiyatli') 
                    return redirect('cars')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
            else:
                forms = CarBrendsForm()
            return render(request, 'admins/mashina/carbreand_input.html', {'forms': forms, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz') 

@login_decorator
def caryear_input(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            if request.method == 'POST':
                forms = CarYearForm(request.POST, request.FILES)
                if forms.is_valid():
                    forms.save()
                    messages.success(request, 'Muvafaqiyatli') 
                    return redirect('cars')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
            else:
                forms = CarYearForm()
            return render(request, 'admins/mashina/caryear_input.html', {'forms': forms, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz') 

@login_decorator
def carprice_input(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            if request.method == 'POST':
                forms = CarPriceForm(request.POST, request.FILES)
                if forms.is_valid():
                    forms.save()
                    messages.success(request, 'Muvafaqiyatli') 
                    return redirect('cars')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
            else:
                forms = CarPriceForm()
            return render(request, 'admins/mashina/carprice_input.html', {'forms': forms, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz') 

@login_decorator
def manzil_input(request):
    try:
        if request.user.admin_profile.is_admin:
            application = Review.objects.all().filter(status='yangi')
            if request.method == 'POST':
                forms = Manzil1Form(request.POST, request.FILES)
                form = Manzil2Form(request.POST, request.FILES)
                if forms.is_valid() and form.is_valid():
                    forms.save()
                    form.save()
                    messages.success(request, 'Muvafaqiyatli') 
                    return redirect('cars')  # O'zgartirilgan profilingiz ro'yxati sahifasiga yo'naltiriladi
            else:
                forms = Manzil1Form()
                form = Manzil2Form()
            return render(request, 'admins/mashina/manzil_input.html', {'forms': forms, 'form': form, 'application':application})
    except:
        messages.warning(request, 'Siz admin emasiz') 


@login_decorator
def full_appl(request):
    application = Review.objects.all().filter(status='yangi')
    appls = Review.objects.all()  
    ctx = {'appls': appls, 'applicatons': application}
    return render(request, 'admins/applications/new_application.html', ctx)    

@login_decorator
def new_appl(request):
    application = Review.objects.all().filter(status='yangi')
    appls = Review.objects.all().filter(status='yangi')
    print(appls)
    ctx = {'appls': appls, 'application': application}
    return render(request, 'admins/applications/new_application.html', ctx)    

@login_decorator
def conf_appl(request):
    application = Review.objects.all().filter(status='yangi')
    appls = Review.objects.all().filter(status='berildi')
    ctx = {'appls': appls, 'application':application}
    return render(request, 'admins/applications/new_application.html', ctx)    

@login_decorator
def retu_appl(request):
    application = Review.objects.all().filter(status='yangi')
    appls = Review.objects.all().filter(status='qaytarildi')  
    ctx = {'appls': appls, 'application':application}
    return render(request, 'admins/applications/new_application.html', ctx)    


@login_decorator
def refuse_appl(request):
    application = Review.objects.all().filter(status='yangi')
    appls = Review.objects.all().filter(status='rad etildi') 
    ctx = {'appls': appls, 'application':application}
    return render(request, 'admins/applications/new_application.html', ctx)   

@login_decorator
def edit_appl(request, pk):
    application = Review.objects.all().filter(status='yangi')
    appls = Review.objects.get(pk=pk)
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        forms = ReviewForm(request.POST, instance=review)
        if forms.is_valid():
            forms.save()
            return redirect('full_appl')
    else:
        forms = ReviewForm(instance=review)
    ctx = {'appls': appls, 'application':application, 'forms':forms}
    return render(request, 'admins/applications/edit_application.html', ctx)   
