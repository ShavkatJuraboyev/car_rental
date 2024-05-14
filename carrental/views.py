from django.shortcuts import render, redirect
from carrental.models import CarBrends, CarModels, CarPrice, CarYear, Cars, CarRentai, Review, Booking, Manzil1, Manzil2
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, CarRentaiForm
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
import random, string, os, http.client
# Create your views here.

def login_decorator(func):
    return login_required(func, login_url='login')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'} 

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        car_form = CarRentaiForm(request.POST, request.FILES)

        if form.is_valid() and car_form.is_valid():
            user = form.save()
            car = car_form.save(commit=False)  # Don't save yet
            car.user = user  # Associate the CarRentai instance with the user
            car.save()  # Save the CarRentai instance

            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} foydalanuvchi yaratildi')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.warning(request, f'{field}: {error}')

        return render(request, 'users/register.html', {'form': form})



def login_user(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, password=password, username=username)
            
            if user is not None:
                try:
                    login(request, user)
                    messages.success(request, f'Tizimga muvafaqiyatli kirdingiz!')
                    return redirect('home')
                except:
                    messages.warning(request, f'Siz foydalanuvchilar ro\'yxatidan o\'tmagansiz! \n Iltimos avval ro\'yxatdan o\'ting!')
                    return redirect("home")
            else:
                messages.warning(request, f'Username yoki parol xato')
                return redirect("login")
                

        else:
            messages.warning(request, f'Forma noto\'g\'ri to\'ldirilgan')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_decorator
def logout_user(request):
    logout(request)
    return redirect("home")



def home(request):
    carbrends = CarBrends.objects.all()
    carmodels = CarModels.objects.all()
    caryears = CarYear.objects.all()
    cars = Cars.objects.all()[:8]

    selected_brend = request.GET.get('brend')
    selected_model = request.GET.get('model')
    selected_year = request.GET.get('year')

    if selected_brend:
        cars = cars.filter(carmodels__carbrends__id=selected_brend)
    if selected_model:
        cars = cars.filter(carmodels__id=selected_model)
    if selected_year:
        cars = cars.filter(caryear__id=selected_year)

    ctx = {
        'carmodels': carmodels,
        'caryears': caryears,
        'carbrends': carbrends,
        'cars': cars,
    }
    return render(request, 'users/index.html', ctx)


# def get_models(request):z


def about(request):
    return render(request, 'users/about.html')


def pricing(request):
    cars = Cars.objects.all()
    ctx = {"cars": cars}
    return render(request, 'users/pricing.html', ctx)


def car(request):
    cars = Cars.objects.all()
    ctx = {'cars': cars}
    return render(request, 'users/car.html', ctx)


def blog(request):
    return render(request, 'users/blog.html')


def contact(request):
    return render(request, 'users/contact.html')


def car_single(request, pk):
    cars = Cars.objects.get(pk=pk)
    reviews = Review.objects.select_related('carrentai', 'cars').filter(cars=cars.id)
    related_cars = Cars.objects.filter(carmodels__carbrends__name=cars.carmodels.carbrends.name).exclude(id=pk)
    print(reviews)
    ctx ={'cars': cars, 'reviews': reviews, 'related_cars': related_cars}
    return render(request, 'users/car-single.html', ctx)


def blog_single(request):
    return render(request, 'users/blog-single.html')


@login_decorator
def checkout(request, pk):
    cars = Cars.objects.get(pk=pk)
    rewiews = Review.objects.all()
    manzil22 = Manzil2.objects.all()
    manzil11 = Manzil1.objects.all()
    if request.method == 'POST':
        manzil1 = request.POST.get('manzil1')
        manzil2 = request.POST.get('manzil2')
        sana1 = request.POST.get('sana1')
        sana2 = request.POST.get('sana2')
        vaqt = request.POST.get('vaqt')
        car_id = request.POST.get('car')

        sms_code = str(random.randint(100000, 999999))
        request.session['sms_code'] = sms_code
        print(sms_code)

        
        # Sessionga ma'lumotlarni saqlash
        request.session['manzil1'] = manzil1
        request.session['manzil2'] = manzil2
        request.session['sana1'] = sana1
        request.session['sana2'] = sana2
        request.session['vaqt'] = vaqt
        request.session['car_id'] = car_id

        return redirect('confirmation')

    return render(request, 'users/checkout.html', {'cars': cars, 'rewiews': rewiews, 'manzil22':manzil22, 'manzil11': manzil11})


@login_decorator
def confirmation(request):
    carrentai = CarRentai.objects.get(user=request.user)
    sms_code = request.session.get('sms_code')
    if request.method == 'POST':
        # Sessiyadan ma'lumotlarni olish
        sms_kod = request.POST.get('sms_kod')
        print(sms_kod)
        if sms_kod == sms_code:
            manzil1 = request.session.get('manzil1')
            manzil2 = request.session.get('manzil2')
            sana1 = request.session.get('sana1')
            sana2 = request.session.get('sana2')
            vaqt = request.session.get('vaqt')
            car_id = request.session.get('car_id')
                
            # Foydalanuvchidan kiritilgan sanani to'g'ri formatga o'tkazish
            correct_date1 = datetime.strptime(sana1, "%m/%d/%Y").strftime("%Y-%m-%d")
            correct_date2 = datetime.strptime(sana2, "%m/%d/%Y").strftime("%Y-%m-%d")

            # Buyurtmani saqlash
            manzil11 = Manzil1.objects.get(pk=manzil1)
            manzil22 = Manzil2.objects.get(pk=manzil2)
            booking_instance = Booking.objects.create(
                manzil1=manzil11,
                manzil2=manzil22,
                sana1=correct_date1,
                sana2=correct_date2,
                vaqt=vaqt,
            )

            car = Cars.objects.get(pk=car_id)
            review_instance = Review.objects.create(
                carrentai = carrentai,
                booking = booking_instance,
                cars=car,
            )
            return redirect('home')
        else:
            return redirect('confirmation')
        return redirect('home')
    return render(request, 'users/sms_paket.html', {'carrentai':carrentai})
    

    
