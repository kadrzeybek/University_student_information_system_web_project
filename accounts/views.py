from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from accounts.models import Users

def login_view(request):
    error_message = None
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Users.objects.filter(username=username).first()

        # Role-Based Authentication
        # if user and check_password(password, user.password_hash):
        if user and password == user.password_hash:
            request.session['user_id'] = user.user_id
            if user.role == "student":
                request.session['student_id'] = user.student_id
                return redirect('/student/homepage')
            elif user.role == "instructor":
                request.session['instructor_id'] = user.instructor_id
                return redirect('/instructor/homepage')
            else:
                pass
        else:
            error_message = "Invalid username or password"

    return render(request, 'accounts/login.html', {
        'is_login_page': True,
        'error_message': error_message
    })

def logout_view(request):
    request.session.flush()  # Clear user data
    response = redirect('index')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response