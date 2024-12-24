from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category,Content
from django.contrib import messages

@never_cache    #avoids caching and prevents opening webpage after clicking back button
@login_required(login_url='/authentication/login')
def index(request):
    categories=Category.objects.all()
    content=Content.objects.filter(owner=request.user)
    context={
        "content":content
    }
    return render(request,'content/index.html',context)

def add(request):
    categories=Category.objects.all()
    context={'categories':categories,'values':request.POST}
    if request.method=="GET":
        return render(request,'content/add.html',context)
    if request.method=="POST":
        amount=request.POST['amount']
        description=request.POST['description']
        category=request.POST['category']
        date=request.POST['date']
        if not amount or not description or not category :
            messages.error(request,'Please fill in all fields')
            return render(request,'content/add.html',context)
        Content.objects.create(owner=request.user,amount=amount,date=date,category=category,description=description)
        messages.success(request,"Data added successfully")
        return redirect('content')

def content_edit(request,id):
    content=Content.objects.get(id=id)
    categories=Category.objects.all()
    context={
        'content':content,
        'values':content,
        'categories':categories
    }
    if request.method=="GET":
        return render(request,'content/edit-content.html',context)
    if request.method=="POST":
        amount=request.POST['amount']
        description=request.POST['description']
        category=request.POST['category']
        date=request.POST['date']
        if not amount or not description or not category :
            messages.error(request,'Please fill in all fields')
            return render(request,'content/edit-content.html',context)
        content.owner=request.user
        content.amount=amount
        content.date=date
        content.category=category
        content.description=description
        content.save()
        messages.success(request,"Data updated successfully")
        return redirect('content')

def content_delete(request,id):    #Add confirmation model before deleting..
    content=Content.objects.get(pk=id)
    content.delete()
    messages.success(request,"Data has been removed")
    return redirect('content')

