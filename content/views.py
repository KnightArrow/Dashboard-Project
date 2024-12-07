from django.shortcuts import render

def index(request):
    return render(request,'content/index.html')

def add(request):
    return render(request,'content/add.html')
