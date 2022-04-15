from django import forms
from django.contrib.auth import get_user_model
from .models import CustomSession
from .admin import UserCreationForm


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'user_name', 'phone_no', 'tower_no', 'flat_no', 'password1', 'password2']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class OtpVerificationForm(forms.ModelForm):
    class Meta:
        model = CustomSession
        fields = ['otp_field']


class UserPasswordResetForm(forms.Form):
    email = forms.EmailField()


class UserNewPasswordConfirmForm(UserCreationForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['password', 'password1', 'password2']
