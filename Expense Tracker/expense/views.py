from django.shortcuts import render
from datetime import date
from django.views.generic import ListView,DetailView
from django.views import View
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .process_file import processfile
from django.db.models import Sum
import json

from .models import Expenses, MerchantCategory
from .forms import CategoryForm

class StartingPageView(View):
    
    def get(self,request):
        return render(request,'expense/index.html')
        
    
    def post(self,request):
        
        statement_file = request.FILES.get('bankstatement')
        
        if statement_file:
            print("File uploaded:", statement_file.name)
            processfile(statement_file)
        else:
            print("Not found!")
        
        return render(request,'expense/index.html')
    
    
class AllTransactionsView(View):
    
    def get(self,request,pageno=None):
        
        if pageno==None:
            return HttpResponseRedirect(reverse("transactions-page",args=[1]))
        
        form = CategoryForm(instance=Expenses)
        expenses = Expenses.objects.all().order_by('-txn_date')
        categories = MerchantCategory.objects.values('category').distinct()
        total_txns = len(expenses)
        lastpage = int(total_txns/20)
        
        if pageno<1:
            return HttpResponseRedirect(reverse("transactions-page",args=[1]))
        if pageno>lastpage and lastpage!=0:
            return HttpResponseRedirect(reverse("transactions-page",args=[lastpage]))
        
        if pageno*20<total_txns:
            expenses = expenses[pageno*20-20:pageno*20+1]
        elif pageno*20-20 < total_txns:
            expenses = expenses[pageno*20-20:]
        elif total_txns>=20:
            expenses = expenses[total_txns-20:]
            
        if pageno-5<=0:
            pg_range = range(1,min(6,lastpage+1))
        elif pageno+5>=lastpage:
            pageno = lastpage
            pg_range = range(max(1,lastpage-4),lastpage+1)
        else:
            pg_range = range(pageno-4,pageno+1)
        
        prevpage = max(pageno-10,1)
        
        context = {
            'transactions': expenses,
            'pageno': pageno,
            'range': pg_range,
            'prevpage': prevpage,
            'form': form,
            'categories': categories
        }
        
        return render(request,"expense/transactions.html",context)
    
    def post(self,request,pageno):
        
        expense_instance = Expenses.objects.get(pk=request.POST['pk'])
        category = CategoryForm(request.POST,instance=expense_instance)
        
        if category.is_valid():
            category.save(commit=True)
            
        print(category.errors)
        return HttpResponseRedirect(reverse("transactions-page",args=[pageno]))
            
    

class DashboardView(View):
    
    def get(self,request):
        
        expense_data = (Expenses.objects.values('merchantobject__category')
        .annotate(total_amount=Sum('txn_amount'))
        .order_by('-total_amount'))
        
        balance_data = Expenses.objects.values('balance')
        
        categories = [item['merchantobject__category'] for item in expense_data if item['total_amount'] < 0]
        amounts = [-item['total_amount'] for item in expense_data if item['total_amount'] < 0]
        balances = [item['balance'] for item in balance_data]
        num = [i for i in range(1,len(balances)+1)]
        
        categories = json.dumps(categories)
        amounts = json.dumps([float(amount) for amount in amounts])
        balances = json.dumps([float(balance) for balance in balances])
        num = json.dumps(num)

        
        
        context = {
            "categories": categories,
            "amounts": amounts,
            "balances": balances,
            "num": num
        }
        
        return render(request,"expense/dashboard.html",context)
    
   
    