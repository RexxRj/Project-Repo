from django.db import models

# Create your models here.

class MerchantCategory(models.Model):
    
    merchant = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.merchant} - {self.category}"

class Expenses(models.Model):
    txn_date = models.DateField()
    desc = models.CharField(max_length=200)
    cheque_no = models.BigIntegerField(null=True)
    txn_amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    merchant = models.CharField(max_length=50)
    merchantobject = models.ForeignKey(MerchantCategory,on_delete=models.SET_NULL, null=True)
    
    
    def __str__(self):
        return f"{self.txn_date} - {self.cheque_no}"
    
