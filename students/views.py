from django.shortcuts import render

def profil_view(request):
    return render(request,'students/profile.html')