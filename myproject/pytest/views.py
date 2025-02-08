from django.shortcuts import render, redirect
from django.contrib import auth, messages
from .models import Service, User
from . import cal
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'services': services})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='login')
def calculator(request):
    result = ""
    if request.method == 'POST':
        num1 = request.POST.get('num1')
        num2 = request.POST.get('num2')
        operation = request.POST.get('operation')
        
        if num1 and num2 and operation:
            result = cal.calculator(num1, operation, num2)
        else:
            result = "Please enter both numbers and choose an operation"

    return render(request, 'calculator.html', {'result': result})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and not user.is_staff:
            auth.login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
    
    
# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username').lower()
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
        
#         if password1 == password2:
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username already exists')
#                 return redirect('register')
#             elif User.objects.filter(email=email).exists():
#                 messages.error(request, 'Email already exists')
#                 return redirect('register')
#             elif ' ' in username:
#                 messages.error(request, 'Username Cannot Contain Spaces')
#                 return redirect('register')
#             else:
#                 user = User.objects.create_user(
#                     username=username,
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                     password=password1
#                 )
#                 user.save()
#                 messages.success(request, 'Account created successfully! Please sign in.')
#                 return redirect('login')
#         else:
#             messages.error(request, 'Passwords do not match')
#             return redirect('register')
#     else:   
#         return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        new_username = request.POST.get('username').lower()
        new_email = request.POST.get('email')
        new_first_name = user.first_name = request.POST.get('first_name')
        new_last_name = user.last_name = request.POST.get('last_name')
        new_age = user.age = request.POST.get('age')
        # Check if username exists but ignore current user
        if User.objects.filter(username=new_username).exclude(id=user.id).exists():
            messages.error(request, 'Username already exists')
            return redirect('profile')
            
        # Check if email exists but ignore current user
        if User.objects.filter(email=new_email).exclude(id=user.id).exists():
            messages.error(request, 'Email already exists')
            return redirect('profile')
        
        if len(new_first_name) > 20 or len(new_last_name) > 20:
            messages.error(request, 'Maximum Character Length 20 Characters')
            return redirect('profile')
        
        if ' ' in new_username:
            messages.error(request, 'Username Cannot Contain Spaces')
            return redirect('profile')
        
        if new_age == '':
            new_age = None
    
        user.username = new_username
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.email = new_email
        user.gender = request.POST.get('gender')
        user.age = new_age
            
        if 'pic' in request.FILES:
            user.pic = request.FILES.get('pic')
            
        try:    
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        return redirect('profile')

    return render(request, 'profile.html', {'user': user})

@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=request.user.id)
            auth.logout(request)
            user.delete()
            messages.success(request, 'Your account has been deleted successfully')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('settings')
    return redirect('settings')

@login_required(login_url='login')
def settings_view(request):
    return render(request, 'settings.html', {'user': request.user})
    