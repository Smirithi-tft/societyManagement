from django.shortcuts import render


def home(request):
    return render(request, 'residents/home.html', {'title': 'Home Page'})
