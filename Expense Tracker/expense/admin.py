from django.contrib import admin

from .models import Expenses,MerchantCategory,Budget

class ExpensesAdmin(admin.ModelAdmin):
    list_filter = ("txn_date","merchantobject__category", "merchant", )
    list_display = ("txn_date", "merchant", "merchantobject")

class MerchantCategoryAdmin(admin.ModelAdmin):
    list_filter = ("merchant", "category")
    list_display = ("merchant", "category")

class BudgetAdmin(admin.ModelAdmin):
    list_filter = ("date",)
    list_display = ("date", "essential", "investment", "non_essential", "savings")

# Register your models here.

admin.site.register(Expenses, ExpensesAdmin)
admin.site.register(MerchantCategory,MerchantCategoryAdmin)
admin.site.register(Budget,BudgetAdmin)
