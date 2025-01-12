from django.shortcuts import render,redirect
from .models import Source,Content1
from django.core.paginator import Paginator
from currencies.models import Currencies
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import json
from django.http import JsonResponse,HttpResponse
import datetime,csv
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum
import os

@never_cache
@login_required(login_url='/authentication/login')
def index(request):
    sources=Source.objects.all()
    content=Content1.objects.filter(owner=request.user)
    paginator=Paginator(content,2,error_messages={"no_results": "Page does not exist"}) #. Available error message keys are: invalid_page, min_page, and no_results.
    #orphans (default: 0): The minimum number of items allowed on the last page. If the number of items on the last page is less than orphans, they are included on the previous page instead.
    #Example: Paginator(queryset, 10, orphans=3).
    #Example: Paginator(queryset, 10, allow_empty_first_page=False).
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number) #or could be Paginator.get_page(paginator,page_number)
    currency=Currencies.objects.get(user=request.user).currency
    context={
        "content1":content,
        'page_obj':page_obj,
        'currency':currency
    }
    return render(request,'content1/index.html',context)

@login_required(login_url='/authentication/login')
def add(request):
    sources=Source.objects.all()
    context={'sources':sources,'values':request.POST}
    if request.method=="GET":
        return render(request,'content1/add.html',context)
    if request.method=="POST":
        amount=request.POST['amount']
        description=request.POST['description']
        source=request.POST['source']
        date=request.POST['content1_date']
        if not amount or not description or not source :
            messages.error(request,'Please fill in all fields')
            return render(request,'content1/add.html',context)
        Content1.objects.create(owner=request.user,amount=amount,date=date,source=source,description=description)
        messages.success(request,"Data added successfully")
        return redirect('content1')

@login_required(login_url='/authentication/login')
def content1_edit(request,id):
    content=Content1.objects.get(id=id)
    sources=Source.objects.all()
    context={
        'content1':content,
        'values':content,
        'sources':sources
    }
    if request.method=="GET":
        return render(request,'content1/edit-content1.html',context)
    if request.method=="POST":
        amount=request.POST['amount']
        description=request.POST['description']
        source=request.POST['source']
        date=request.POST['date']
        if not amount or not description or not source :
            messages.error(request,'Please fill in all fields')
            return render(request,'content1/edit-content1.html',context)
        content.amount=amount
        content.date=date
        content.source=source
        content.description=description
        content.save()
        messages.success(request,"Data updated successfully")
        return redirect('content1')

@login_required(login_url='/authentication/login')
def content1_delete(request,id):    #Add confirmation model before deleting..
    content=Content1.objects.get(id=id)
    content.delete()
    messages.success(request,"Data has been removed")
    return redirect('content1')

def search_content1(request):
    if request.method=="POST":
        decoded_data = (request.body).decode('utf-8')
        search_query=json.loads(decoded_data).get('searchText')
        content=Content1.objects.filter(amount__istartswith=search_query,owner=request.user) | Content1.objects.filter(date__istartswith=search_query,owner=request.user) | Content1.objects.filter(description__icontains=search_query,owner=request.user) | Content1.objects.filter(source__icontains=search_query,owner=request.user)
        data=content.values()
        return JsonResponse(list(data),safe=False)
    
@login_required(login_url='/authentication/login')
def content1_summary_by_source(request):
    todays_date=datetime.date.today()
    last_six_months=todays_date-datetime.timedelta(days=30*6)
    contents=Content1.objects.filter(owner=request.user,date__gte=last_six_months,date__lte=todays_date)
    context={}
    def get_source(content):
        return content.source
    source_list=list(set(map(get_source,contents)))
    def get_source_aggregate(source):
        amount=0
        filtered_by_source=contents.filter(source=source)
        for item in filtered_by_source:
            amount+=item.amount
        return amount
    for content in contents:
        for source in source_list:
            context[source]=get_source_aggregate(source)
    return JsonResponse({'content1_source_data':context},safe=False)

def stas_view(request):
    return render(request,'content1/stats.html')

#CSV Export
def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; fileName=Content1'+str(datetime.datetime.now())+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Amount','Date','Source','Description'])
    contents=Content1.objects.filter(owner=request.user)
    for content in contents:
        writer.writerow([content.amount,content.date,content.source,content.description])
    return response

#Excel Export
def export_excel(request):
    response=HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; fileName=Content1'+str(datetime.datetime.now())+'.xls'
    wb=xlwt.Workbook(encoding='utf-8')
    ws=wb.add_sheet('Content1')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold=True
    columns=['Amount','Date','Source','Description']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    font_style=xlwt.XFStyle()
    rows=Content1.objects.filter(owner=request.user).values_list('amount','date','source','description')
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
    response['Content-Disposition'] = f'inline;attachment; filename=Content1_{timestamp}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    contents=Content1.objects.filter(owner=request.user)
    sum=contents.aggregate(Sum('amount'))
    html_string = render_to_string('content1/pdf-output-content1.html', {'contents': contents, 'total': sum['amount__sum']})
    html = HTML(string=html_string)
    pdf_content = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as output:
        output.write(pdf_content)
        temp_file_path = output.name
    with open(temp_file_path, 'rb') as pdf_file:
        response.write(pdf_file.read())
    os.remove(temp_file_path)

    return response
