from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse

class UsernameValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters.'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username already exists.'},status=400)
        return JsonResponse({'username_valid':True})
class EmailValidationView(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Email already exists.'},status=400)
        return JsonResponse({'email_valid':True})
class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
