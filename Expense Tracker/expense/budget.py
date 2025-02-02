from dateutil.relativedelta import relativedelta
from datetime import datetime
from decimal import Decimal

from .models import Budget,Expenses

def budgetCalculation(recalculate=False):
    
    print("Budget Calculation Started")
    
    if recalculate:
        Budget.objects.all().delete()
    
    expenses = Expenses.objects.all().order_by('txn_date')
    start_date = expenses[0].txn_date
    end_date = expenses[len(expenses)-1].txn_date
    
    current_date = datetime(start_date.year, start_date.month, 1).date()
    next_date = current_date + relativedelta(months=1)
    
    while(Budget.objects.filter(date=next_date).exists()):
        print("Budget already calculated for month: ", current_date)
        current_date = current_date + relativedelta(months=1)
        next_date = current_date + relativedelta(months=1)
        if current_date>end_date:
            print("Budget Calculation Completed")
            return
    
    print(current_date,end_date)
    
    while(current_date<=end_date):
        
        print("Calculating Budget for month: ", current_date)
        
        salary = expenses.filter(txn_date__month=current_date.month, txn_date__year=current_date.year).filter(merchantobject__category__iexact='salary').first()
        if not salary:
            print("Salary not found for month: ", current_date)
            print("Budget Calculation Completed")
            return
        
        essential = salary.txn_amount * Decimal('0.5')
        investment = salary.txn_amount * Decimal(0.2)
        non_essential = salary.txn_amount * Decimal(0.2)
        savings = salary.txn_amount * Decimal(0.1)
        
        
        if current_date.month == start_date.month and current_date.year == start_date.year:
            Budget.objects.create(
                date = next_date,
                essential = essential,
                investment = investment,
                non_essential = non_essential,
                savings = savings
            )
        else:
            essential_expenses = expenses.filter(txn_date__month=current_date.month, txn_date__year=current_date.year, merchantobject__category__iexact='essential')
            essential_expenses_total = sum([expense.txn_amount for expense in essential_expenses])
            investment_expenses = expenses.filter(txn_date__month=current_date.month, txn_date__year=current_date.year, merchantobject__category__iexact='investment')
            investment_expenses_total = sum([expense.txn_amount for expense in investment_expenses])
            non_essential_expenses = expenses.filter(txn_date__month=current_date.month, txn_date__year=current_date.year).exclude(
                        merchantobject__category__iexact='essential'
                    ).exclude(
                        merchantobject__category__iexact='investment'
                    ).exclude(
                        merchantobject__category__iexact='salary'
                    )
            non_essential_expenses_total = sum([expense.txn_amount for expense in non_essential_expenses])
            
            prev_budget = Budget.objects.get(date=current_date)
            prev_essential = prev_budget.essential
            prev_investment = prev_budget.investment
            prev_non_essential = prev_budget.non_essential
            prev_savings = prev_budget.savings
            
            essential_expenses_total = essential_expenses_total + prev_essential
            investment_expenses_total = investment_expenses_total + prev_investment
            non_essential_expenses_total = non_essential_expenses_total + prev_non_essential
            
            investment = investment + investment_expenses_total
            non_essential = non_essential + non_essential_expenses_total
            savings = savings + prev_savings
            
            if essential<0:
                essential = essential + essential_expenses_total
                essential_expenses_total = 0
            
            if essential < 0:
                essential = savings + essential
                savings = 0
            
            
            if essential < 0:
                essential = non_essential + essential
                non_essential = 0
                
            if essential < 0:
                essential = investment + essential
                investment = 0
            
            if investment < 0:
                investment = savings + investment
                savings = 0
            
            if investment < 0:
                investment = non_essential + investment
                non_essential = 0
            
            if non_essential <= 0:
                non_essential = savings + non_essential
                savings = 0
                
            if non_essential <= 0:
                non_essential = non_essential + essential_expenses_total
                essential_expenses_total = 0
            
            savings = savings + essential_expenses_total
            
            Budget.objects.create(
                date = next_date,
                essential = essential,
                investment = investment,
                non_essential = non_essential,
                savings = savings
            )
        
        current_date = next_date
        next_date = current_date + relativedelta(months=1)
    
    print("Budget Calculation Completed")
    return
    

    
