from django.shortcuts import render
from datetime import date
from django.views.generic import ListView,DetailView
from django.views import View
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .process_file import processfile
from django.db.models import Sum
import json
from datetime import datetime

from .models import Expenses, MerchantCategory
from .forms import AddCategoryForm,EditCategoryForm

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
        
        # Fetch selected filters
        selected_merchant = request.GET.get('merchant', '')
        selected_category = request.GET.get('category', '')
        selected_start_date = request.GET.get('start_date', '')
        selected_end_date = request.GET.get('end_date', '')
        
        # Prepare filter conditions
        filters = {}

        if selected_merchant:
            filters['merchant'] = selected_merchant
        if selected_category:
            filters['merchantobject__category'] = selected_category
        if selected_start_date:
            filters['txn_date__gte'] = datetime.strptime(selected_start_date, '%Y-%m-%d')
        if selected_end_date:
            filters['txn_date__lte'] = datetime.strptime(selected_end_date, '%Y-%m-%d')
        
        form = AddCategoryForm(instance=Expenses)
        expenses = Expenses.objects.all().order_by('-txn_date')
        if len(expenses)>0:
            current_balance = expenses[0].balance
        else:
            current_balance = 0
        expenses = expenses.filter(**filters)
        categories = MerchantCategory.objects.values('category').distinct()
        merchants = expenses.values('merchant').distinct()
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
            pg_range = range(1,min(6,max(lastpage+1,2)))
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
            'categories': categories,
            'merchants': merchants,
            'current_balance': current_balance,
            'selected_merchant': selected_merchant,
            'selected_category': selected_category,
            'selected_start_date': selected_start_date,
            'selected_end_date': selected_end_date,
        }
        
        
        
        return render(request,"expense/transactions.html",context)
    
    def post(self,request,pageno):
        
        if request.POST['action'] == 'delete':
            
            print(request.POST)
            selected_merchant = request.POST.get('merchant', '')
            selected_category = request.POST.get('category', '')
            selected_start_date = request.POST.get('start_date', '')
            selected_end_date = request.POST.get('end_date', '')
            
            
            
            # Prepare filter conditions
            filters = {}

            if selected_merchant:
                filters['merchant'] = selected_merchant
            if selected_category:
                filters['merchantobject__category'] = selected_category
            if selected_start_date:
                filters['txn_date__gte'] = datetime.strptime(selected_start_date, '%Y-%m-%d')
            if selected_end_date:
                filters['txn_date__lte'] = datetime.strptime(selected_end_date, '%Y-%m-%d')
                
            expense_instance = Expenses.objects.filter(**filters)
            expense_instance.delete()
            # print(expense_instance)
            print('deleted')
            return HttpResponseRedirect(reverse("transactions-page",args=[pageno]))
            
        expense_instance = Expenses.objects.get(pk=request.POST['pk'])
        category = AddCategoryForm(request.POST,instance=expense_instance)
        
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
    
   

class CategoriesView(View):
    
    def get(self,request,pageno=None):
        
        if pageno==None:
            return HttpResponseRedirect(reverse("categories-page",args=[1]))
        
        categories = MerchantCategory.objects.all()
        total_txns = len(categories)
        lastpage = int(total_txns/20)
        
        if pageno<1:
            return HttpResponseRedirect(reverse("categories-page",args=[1]))
        if pageno>lastpage and lastpage!=0:
            return HttpResponseRedirect(reverse("categories-page",args=[lastpage]))
        
        if pageno*20<total_txns:
            categories = categories[pageno*20-20:pageno*20+1]
        elif pageno*20-20 < total_txns:
            categories = categories[pageno*20-20:]
        elif total_txns>=20:
            categories = categories[total_txns-20:]
            
        if pageno-5<=0:
            pg_range = range(1,min(6,max(lastpage+1,2)))
        elif pageno+5>=lastpage:
            pageno = lastpage
            pg_range = range(max(1,lastpage-4),lastpage+1)
        else:
            pg_range = range(pageno-4,pageno+1)
        
        prevpage = max(pageno-10,1)
        
        return render(request,'expense/categories.html',{
            'categories':categories,
            'pageno': pageno,
            'range': pg_range,
            'prevpage': prevpage,
            })
        
    def post(self,request,pageno=None):
        
        if request.POST.get('action') == 'delete':
            
            default_merchantobj = MerchantCategory.objects.get(merchant='default')
            instance = MerchantCategory.objects.get(pk=request.POST.get('id'))
            if default_merchantobj:
                Expenses.objects.filter(merchantobject=instance).update(merchantobject=default_merchantobj)
            instance.delete()
            return HttpResponseRedirect(reverse("categories-page"))
        
        categoryform = EditCategoryForm(request.POST)

        
        if categoryform.is_valid():
            categoryform.save()

        
        return HttpResponseRedirect(reverse("categories-page",args=[pageno]))
        
        
            