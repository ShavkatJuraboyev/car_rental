from django import forms
from dashboard.models import AdminProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from carrental.models import Cars, CarModels, CarBrends, CarYear, CarPrice, Manzil1, Manzil2, Review


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class AdminProfileForm1(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['is_admin', 'is_self_visible', 'user']
        widgets = {
            "is_admin": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_self_visible": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "user": forms.Select(attrs={'class': 'form-control'})
        }


class AdminProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = AdminProfile
        fields = '__all__'
        exclude = ['user']

    def clean_email(self):
        email = self.cleaned_data['email']
        if "example.com" in email:
            raise forms.ValidationError("Example.com manzilini ishlatmaslik kerak")
        return email



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}))


class CarsFrom(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['is_konditsioner','is_gps','is_bagaj','is_musiqa','is_kamar','is_audio_kiritsh','is_bluethooth','is_uzoq_masofa','is_uxlash_stoli','is_kalit_plut','is_bortli_kompyuter', 'carmodels', 'caryear', 'carprices','image','kilometers','mator','sat_down','baggage','fuel','description',]
        widgets = {
            "is_konditsioner": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_gps": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_bagaj": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_musiqa": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_kamar": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_audio_kiritsh": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_bluethooth": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_uzoq_masofa": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_uxlash_stoli": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_kalit_plut": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "is_bortli_kompyuter": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            "image": forms.FileInput(attrs={'class': 'form-control'}),
            "kilometers": forms.NumberInput(attrs={'class': 'form-control'}),
            "mator": forms.TextInput(attrs={'class': 'form-control'}),
            "sat_down": forms.NumberInput(attrs={'class': 'form-control'}),
            "baggage": forms.TextInput(attrs={'class': 'form-control'}),
            "fuel": forms.TextInput(attrs={'class': 'form-control'}),
            "description": forms.TextInput(attrs={'class': 'form-control'}),
            "carmodels": forms.Select(attrs={'class': 'form-control'}),
            "caryear": forms.Select(attrs={'class': 'form-control'}),
            "carprices": forms.Select(attrs={'class': 'form-control'}),
        }

class CarModelsForm(forms.ModelForm):
    class Meta:
        model = CarModels
        fields = ['name','carbrends']
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "carbrends": forms.Select(attrs={'class': 'form-control'}),
        }

class CarBrendsForm(forms.ModelForm):
    class Meta:
        model = CarBrends
        fields = ['name']
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'})
        }

class CarYearForm(forms.ModelForm):
    class Meta:
        model = CarYear
        fields = ['name']
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'})
        }

class CarPriceForm(forms.ModelForm):
    class Meta:
        model = CarPrice
        fields = ['price_1','price_2','price_3',]
        widgets = {
            "price_1": forms.TextInput(attrs={'class': 'form-control'}),
            "price_2": forms.TextInput(attrs={'class': 'form-control'}),
            "price_3": forms.TextInput(attrs={'class': 'form-control'}),
        }

class Manzil1Form(forms.ModelForm):
    class Meta:
        model = Manzil1
        fields = ['manzil1']
        widgets = {
            "manzil1": forms.TextInput(attrs={'class': 'form-control'}),
        }


class Manzil2Form(forms.ModelForm):
    class Meta:
        model = Manzil2
        fields = ['manzil2']
        widgets = {
            "manzil2": forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['status']
        widgets = {
            "status": forms.Select(attrs={'class': 'form-control'}),
        }