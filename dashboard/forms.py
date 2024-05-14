from django import forms
from dashboard.models import AdminProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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