from django.shortcuts import render, redirect
from accounts.models import Users

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Users.objects.filter(username=username).first()

        if user:
            request.session['user_id'] = user.user_id
            if user.role == "student":
                return redirect('grades')  # students/urls.py'da name='profil'
            elif user.role == "instructor":
                # Burada instructor için bir profil veya ana sayfa view'ı oluşturup yönlendirebilirsin
                return redirect('/')  # Örnek: instructor ana sayfası
            else:
                # Diğer roller için yönlendirme veya hata mesajı
                pass
        

    return render(request, 'accounts/login.html')