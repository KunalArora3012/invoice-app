from django.shortcuts import render, redirect
from .models import Employee
from django.contrib.auth.hashers import make_password, check_password


def signup_view(request):
    if request.method == "POST":
        Employee.objects.create(
            name=request.POST['name'],
            address=request.POST['address'],
            contact=request.POST['contact'],
            emp_id=request.POST['emp_id'],
            department=request.POST['department'],
            username=request.POST['username'],
            password=make_password(request.POST['password'])  # 🔐 HASHED
        )
        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = Employee.objects.get(username=username)

            if check_password(password, user.password):   # 🔐 VERIFY
                request.session['user'] = user.username
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'error': 'Wrong Password'})

        except Employee.DoesNotExist:
            return render(request, 'login.html', {'error': 'User not found'})

    return render(request, 'login.html')

def dashboard_view(request):
    if 'user' not in request.session:
        return redirect('login')

    user = Employee.objects.get(username=request.session['user'])
    return render(request, 'dashboard.html', {'user': user})

def logout_view(request):
    request.session.flush()
    return redirect('login')