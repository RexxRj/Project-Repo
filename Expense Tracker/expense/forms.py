from django import forms

from .models import MerchantCategory,Expenses

class AddCategoryForm(forms.ModelForm):
    
    new_category = forms.CharField(required=False)
    
    class Meta:
        model = Expenses
        fields = ['merchantobject']
        exclude = ["merchantobject"]
    
    def save(self, commit = True):
        
        new_category = self.cleaned_data.get('new_category')
        
        merchant = self.instance.merchant
        
        if new_category:
            merchant_category,created = MerchantCategory.objects.get_or_create(
                merchant=merchant,
                category = new_category
            )
            
            self.instance.merchantobject = merchant_category
            Expenses.objects.filter(merchant=merchant).update(merchantobject=merchant_category)
        else:
            print("not working")
        
        return super().save(commit=commit)
    
class EditCategoryForm(forms.ModelForm):
    
    class Meta:
        
        model = MerchantCategory
        fields = '__all__'
    id = forms.IntegerField(widget=forms.HiddenInput())
    
    def save(self, commit = True):
        
        
        pk = self.cleaned_data.get('id')
        category = self.cleaned_data.get('category')
        
        if pk:
            instance = MerchantCategory.objects.get(id=pk)
            instance.category = category
            if commit:
                instance.save()  # Save the updated instance to the database
            return instance
        
        return super().save(commit)