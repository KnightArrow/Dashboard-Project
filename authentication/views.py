from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.core.mail import EmailMessage
from validate_email import validate_email
from django.contrib import messages
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib.auth import login,logout,authenticate

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
        if not validate_email(email):
            return JsonResponse({'email_error':'Invalid Email.'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Email already exists.'},status=400)
        return JsonResponse({'email_valid':True})
class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    def post(self,request):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        context={
            'fieldValues':request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(password=password).exists():
                if len(password)<8:
                    messages.error(request,"Password should be atleast 8 characters long")
                    return render(request,'authentication/register.html',context)
                user=User.objects.create_user(username=username,email=email)    #Account Creation
                user.set_password(password)                                     #Setting Password
                user.is_active=True
                user.save()                                                     #Saving User Detail
                email_subject='Activate your account'
                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                domain=get_current_site(request).domain
                link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                activate_url='http://'+domain+link
                email_body='Hi '+user.username+' Use link to activate your account\n\n'+activate_url
                email = EmailMessage( email_subject,email_body,"noreply@semycolon.com",[email])
                email.send(fail_silently=False)
                messages.success(request,"Account Created Successfully")        #Success Message
        return render(request,'authentication/register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist):
            user=None
        if user is not None and token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account activated Successfully")        #Success Message
            return redirect('login')
        elif not token_generator.check_token(user,token):
            return redirect('login')
        elif user.is_active:
            return redirect('login')
        else:
            messages.error(request,'Account link invalid')
            return redirect('login')
class LoginView(View):
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        if username and password:
            user=authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    messages.success(request,'Welcome, '+username+' You are now logged in')
                    return redirect('content')
                messages.error(request,"Account is not active, check your email")
                return render(request,'authentication/login.html')
            messages.error(request,"Invalid username or password")
            return render(request,'authentication/login.html')
        messages.error(request,"Please fill all the fields")
        return render(request,'authentication/login.html')

    def get(self,request):
        return render(request,'authentication/login.html')

class LogoutView(View):
    def post(self,request):
        logout(request)
        messages.success(request,"You have been logged out")
        return redirect('login')