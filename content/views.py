from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Category,Content
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse,HttpResponse
from currencies.models import Currencies
#CSV Imports
import datetime,csv
#Excel Imports
import xlwt
#PDF Imports
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum
import os


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
    currency=Currencies.objects.get(user=request.user).currency
    context={
        "content":content,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request,'content/index.html',context)

def search_content(request):
    if request.method=="POST":
        decoded_data = (request.body).decode('utf-8')
        search_query=json.loads(decoded_data).get('searchText')
        content=Content.objects.filter(amount__istartswith=search_query,owner=request.user) | Content.objects.filter(date__istartswith=search_query,owner=request.user) | Content.objects.filter(description__icontains=search_query,owner=request.user) | Content.objects.filter(category__icontains=search_query,owner=request.user)
        data=content.values()
        return JsonResponse(list(data),safe=False)

@login_required(login_url='/authentication/login')
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

@login_required(login_url='/authentication/login')
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

@login_required(login_url='/authentication/login')
def content_delete(request,id):    #Add confirmation model before deleting..
    content=Content.objects.get(pk=id)
    content.delete()
    messages.success(request,"Data has been removed")
    return redirect('content')

# Chat.js 
@login_required(login_url='/authentication/login')
def content_summary_by_category(request):
    todays_date=datetime.date.today()
    last_six_months=todays_date-datetime.timedelta(days=30*6)
    contents=Content.objects.filter(owner=request.user,date__gte=last_six_months,date__lte=todays_date)
    context={}
    def get_category(content):
        return content.category
    category_list=list(set(map(get_category,contents)))
    def get_category_aggregate(category):
        amount=0
        filtered_by_category=contents.filter(category=category)
        for item in filtered_by_category:
            amount+=item.amount
        return amount
    for content in contents:
        for category in category_list:
            context[category]=get_category_aggregate(category)
    return JsonResponse({'content_category_data':context},safe=False)

def stas_view(request):
    return render(request,'content/stats.html')

#CSV Export
def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; fileName=Content'+str(datetime.datetime.now())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount','Date','Category','Description'])
    contents=Content.objects.filter(owner=request.user)
    for content in contents:
        writer.writerow([content.amount,content.date,content.category,content.description])
    return response

#Excel Export
def export_excel(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; fileName=Content'+str(datetime.datetime.now())+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Content')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Amount','Date','Category','Description']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style=xlwt.XFStyle()
    rows=Content.objects.filter(owner=request.user).values_list('amount','date','category','description')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)
    return response

#PDF Export
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    response['Content-Disposition'] = f'inline;attachment; filename=Content_{timestamp}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    contents=Content.objects.filter(owner=request.user)
    sum=contents.aggregate(Sum('amount'))
    html_string = render_to_string('content/pdf-output.html', {'contents': contents, 'total': sum['amount__sum']})
    html = HTML(string=html_string)
    pdf_content = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as output:
        output.write(pdf_content)
        temp_file_path = output.name
    with open(temp_file_path, 'rb') as pdf_file:
        response.write(pdf_file.read())
    os.remove(temp_file_path)

    return response
