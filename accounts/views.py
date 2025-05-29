from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from accounts.models import Users

def login_view(request):
    """
    Handles user authentication and redirects to appropriate homepage based on role.
    
    This view processes login form submissions, validates credentials, and
    establishes user sessions for authorized users.
    """
    error_message = None
    
    if request.method == "POST":
        # Extract user credentials from form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Query database for user with matching username
        user = Users.objects.filter(username=username).first()

<<<<<<< HEAD
        # Role-Based Authentication
        # if user and check_password(password, user.password_hash):
        if user and password == user.password_hash:
=======
        # Verify user exists and password matches
        if user and check_password(password, user.password_hash):
            # Set base user session data
>>>>>>> acd45874edf0632c364328998fd468ddf5b1ed6b
            request.session['user_id'] = user.user_id
            
            # Route user to appropriate dashboard based on role
            if user.role == "student":
                # Store student-specific session data
                request.session['student_id'] = user.student_id
<<<<<<< HEAD
                return redirect('/student/homepage')
=======
                return redirect('/student/homepage')  # Redirect to student dashboard
>>>>>>> acd45874edf0632c364328998fd468ddf5b1ed6b
            elif user.role == "instructor":
                # Store instructor-specific session data
                request.session['instructor_id'] = user.instructor_id
<<<<<<< HEAD
                return redirect('/instructor/homepage')
=======
                return redirect('/instructor/homepage')  # Redirect to instructor dashboard
>>>>>>> acd45874edf0632c364328998fd468ddf5b1ed6b
            else:
                # Future support for additional roles
                pass
        else:
            # Authentication failed - set error message
            error_message = "Invalid username or password"

    # Render login page with error message if authentication failed
    return render(request, 'accounts/login.html', {
        'is_login_page': True,
        'error_message': error_message
    })

def logout_view(request):
<<<<<<< HEAD
    request.session.flush()  # Clear user data
    response = redirect('index')
=======
    """
    Terminates user session and redirects to index page.
    
    This view handles the logout process by clearing all session data
    and setting response headers to prevent caching.
    """
    # Clear all session data for security
    request.session.flush()
    
    # Create redirect response to landing page
    response = redirect('index')
    
    # Add security headers to prevent browser caching of sensitive pages
    # This prevents using the back button to access authenticated content after logout
>>>>>>> acd45874edf0632c364328998fd468ddf5b1ed6b
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response