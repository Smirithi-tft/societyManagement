from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from .forms import UserSignUpForm, UserLoginForm, UserPasswordResetForm, UserNewPasswordConfirmForm, \
    OtpVerificationForm
from .models import CustomSession
from societyManagement.settings import EMAIL_HOST_USER
import random
import math
import pytz
from datetime import datetime


def user_signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.INFO,
                                 message="You must have received a mail. Verify your email to login")
            user = form.save()
            request.session['userid'] = user.id
            request.session['session_key'] = request.session.session_key
            # print(f'session key in sign up: {request.session.session_key}')
            return redirect('send-email')

    if request.user.is_authenticated:
        return redirect('home-page')
    else:
        form = UserSignUpForm()
        return render(request, 'users/sign_up.html', {'title': 'Sign Up', 'form': form})


def send_email(request):
    User = get_user_model()
    user = User.objects.get(pk=request.session['userid'])
    to_email = user.email
    from_email = EMAIL_HOST_USER
    html_message = render_to_string('email_verification.html', {'name': user.user_name, 'email': user.email})
    plain_message = strip_tags(html_message)

    send_mail(
        'Verify your Email',
        plain_message,
        from_email,
        [to_email],
        html_message=html_message
    )
    return render(request, 'users/resend_email.html', {'title': 'Verify user'})


def user_login(request):
    digits = "0123456789"
    otp = ""
    for i in range(4):
        otp += digits[math.floor(random.random() * 10)]
    User = get_user_model()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.get(email=user_email)
            if user.is_active:
                userObj = authenticate(request, email=user_email, password=password)
                if userObj is not None:
                    print(otp)
                    new_session = CustomSession()
                    new_session.session_key = request.session.session_key
                    new_session.otp_field = otp
                    print(f'session object session_key: {new_session.session_key},'
                          f' session object otp: {new_session.otp_field}')
                    new_session.save()
                    send_mail(
                        'OTP Verification',
                        f'Your code is : {otp}',
                        EMAIL_HOST_USER,
                        [user_email],
                        fail_silently=False
                    )
                    return redirect('verify-otp')
                else:
                    return None
            else:
                messages.add_message(request, messages.WARNING,
                                     message="Email not yet verified. Please verify your email to log in.")
                return redirect('verify-email')

    if request.user.is_authenticated:
        return redirect('home-page')
    else:
        form = UserLoginForm()
        return render(request, 'users/login.html', {'title': 'Sign In', 'form': form})


def verify_otp(request):
    User = get_user_model()
    user = User.objects.get(id=request.session['userid'])
    session_obj = CustomSession.objects.filter(session_key=request.session['session_key']).last()
    generated_otp = int(session_obj.otp_field)

    if request.method == 'POST':
        next_url = request.POST.get('next-url')
        user_otp = int(request.POST.get('otp_field'))
        difference_in_seconds = get_time_difference(session_obj.created_time)

        if user_otp == generated_otp and difference_in_seconds <= 30:
            if user.is_active:
                login(request, user)
                if next_url == '':
                    return redirect('home-page')
                else:
                    return redirect(next_url)
            else:
                return None
        else:
            return render(request, 'users/login_fail.html', {'title': 'Login unsuccessful', 'time_diff':
                                                             difference_in_seconds})

    form = OtpVerificationForm()
    return render(request, 'users/verify_otp.html', {'title': 'OTP Verification', 'form': form})


def get_time_difference(obj_date):
    otp_created_date = obj_date

    current_date = datetime.now(pytz.timezone('Asia/Kolkata'))
    time_diff = current_date - otp_created_date
    minutes = divmod(time_diff.seconds, 60)

    return minutes[1]


def verify_email(request):
    User = get_user_model()
    # print(f'session key in verify email: {request.session.session_key}')
    user = User.objects.get(pk=request.session['userid'])
    # print(f'User object from UserModel after sign up: {user}')
    user.is_active = True
    user.save()
    return render(request, 'users/verify_email.html', {'title': 'User verification'})


def password_reset(request):
    User = get_user_model()
    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user = User.objects.get(email=user_email)
            if user is not None:
                messages.add_message(request, messages.INFO,
                                     message="You must have received a mail. Reset your password using the link.")

                request.session['email'] = user_email
                to_email = user_email
                from_email = EMAIL_HOST_USER
                html_message = render_to_string('password_reset_email.html', {'email': user_email})
                plain_message = strip_tags(html_message)

                send_mail(
                    'Reset your password',
                    plain_message,
                    from_email,
                    [to_email],
                    html_message=html_message
                )
                return redirect('home-page')
            else:
                messages.add_message(request, messages.WARNING,
                                     message="Entered email is not registered. Please try again.")
                return redirect('user-signup')

    form = UserPasswordResetForm()
    return render(request, 'users/reset_password.html', {'title': 'Enter your email', 'form': form})


def confirm_password(request):
    User = get_user_model()
    if request.method == 'POST':
        form = UserNewPasswordConfirmForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['password']
            user = User.objects.get(email=request.session['email'])
            if user.check_password(old_password) is not True:
                messages.add_message(request, messages.WARNING,
                                     message="Current password entered is incorrect.")
                return redirect('confirm-password')

            new_password = form.cleaned_data['password2']
            user.set_password(new_password)
            user.save()
            return redirect('user-login')

    else:
        form = UserNewPasswordConfirmForm()
        return render(request, 'users/confirm_password.html', {'title': 'Reset password', 'form': form})
