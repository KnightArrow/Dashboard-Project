from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category,Content
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

@never_cache    #avoids caching and prevents opening webpage after clicking back button
@login_required(login_url='/authentication/login')
def index(request):
    categories=Category.objects.all()
    content=Content.objects.filter(owner=request.user)
    paginator=Paginator(content,2,error_messages={"no_results": "Page does not exist"}) #. Available error message keys are: invalid_page, min_page, and no_results.
    #orphans (default: 0): The minimum number of items allowed on the last page. If the number of items on the last page is less than orphans, they are included on the previous page instead.
    #Example: Paginator(queryset, 10, orphans=3).
    #Example: Paginator(queryset, 10, allow_empty_first_page=False).
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number) #or could be Paginator.get_page(paginator,page_number)
    context={
        "content":content,
        'page_obj':page_obj
    }
    return render(request,'content/index.html',context)

def search_content(request):
    if request.method=="POST":
        search_query=json.loads(request.body).get('searchText')
        content=Content.objects.filter(amount__istartswith=search_query,owner=request.user) | Content.objects.filter(date__istartswith=search_query,owner=request.user) | Content.objects.filter(description__icontains=search_query,owner=request.user) | Content.objects.filter(category__icontains=search_query,owner=request.user)
        data=content.values()
        return JsonResponse(list(data),safe=False)

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

