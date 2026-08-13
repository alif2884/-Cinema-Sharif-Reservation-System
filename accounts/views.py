from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import LoginForm, SignupForm, PhoneEntryForm
from .models import Wallet
from django.db import transaction

def auth_entry(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('admin:index')
        return redirect('movie_list')

    if request.method == 'POST':
        form = PhoneEntryForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            request.session['auth_phone'] = phone
            
            if User.objects.filter(phone_number=phone).exists():
                messages.info(request, f'شماره {phone} شناخته شد. لطفاً رمز عبور را وارد کنید.')
                return redirect('login')
            else:
                messages.info(request, f'شماره {phone} جدید است. لطفاً ثبت‌نام را تکمیل کنید.')
                return redirect('signup')
    else:
        form = PhoneEntryForm()

    return render(request, 'accounts/auth_entry.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('movie_list')

    initial_data = {}
    if 'auth_phone' in request.session:
        initial_data = {'username': request.session.get('auth_phone')}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            input_identifier = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            username_to_auth = input_identifier
            
            try:
                user_obj = User.objects.get(phone_number=input_identifier)
                username_to_auth = user_obj.username
            except User.DoesNotExist:
                pass

            user = authenticate(request, username=username_to_auth, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, '✅ با موفقیت وارد شدید')
                
                if 'auth_phone' in request.session:
                    del request.session['auth_phone']

                if user.is_superuser or user.is_staff:
                    return redirect('admin:index')
                else:
                    return redirect('movie_list')
            else:
                messages.error(request, '❌ نام کاربری یا رمز عبور اشتباه است')
    else:
        form = LoginForm(initial=initial_data)

    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('movie_list')

    initial_data = {}
    if 'auth_phone' in request.session:
        initial_data = {'phone_number': request.session.get('auth_phone')}

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            login(request, user)
            messages.success(request, '🎉 ثبت‌نام با موفقیت انجام شد')
            
            if 'auth_phone' in request.session:
                del request.session['auth_phone']

            return redirect('movie_list')
    else:
        form = SignupForm(initial=initial_data)

    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, '👋 با موفقیت خارج شدید')
    return redirect('auth_entry')

@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect('movie_list')
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def charge_wallet(request):
    if request.method == 'POST':
        amount_raw = request.POST.get('amount', '0')
        try:
            amount = int(amount_raw)
        except (ValueError, TypeError):
            messages.error(request, 'مبلغ وارد شده معتبر نیست.')
            return redirect(request.META.get('HTTP_REFERER', 'movie_list'))

        if amount <= 0:
            messages.error(request, 'مبلغ باید مثبت باشد.')
            return redirect(request.META.get('HTTP_REFERER', 'movie_list'))

        try:
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(user=request.user)
                wallet.balance += amount
                wallet.save()
            
            messages.success(request, f'✅ کیف پول شما {amount} تومان شارژ شد.')
            
        except Wallet.DoesNotExist:
            Wallet.objects.create(user=request.user, balance=amount)
            messages.success(request, f'✅ کیف پول ساخته شد و {amount} تومان شارژ شد.')

    return redirect(request.META.get('HTTP_REFERER', 'movie_list'))