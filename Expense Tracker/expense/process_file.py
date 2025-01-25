from .models import Expenses, MerchantCategory
import pandas as pd

from .ml_models.ml_model_main import PredictModel, TrainModel

def AssignCategoryAI(row):
    merchant = row['user'].lower().strip()
    merchantobj = MerchantCategory.objects.filter(merchant=merchant).first()
    
    
    if not merchantobj:
        
        try:
            predictmod = PredictModel(merchant)
            prediction = predictmod.predict()
            
            created = MerchantCategory.objects.create(
                                
                                merchant=merchant,  
                                category = prediction
                                )
            if created:
                print("A new merchantcategory record was created.")
                merchantobj = created
            else:
                raise RuntimeError("Failed to create new merchantcategory record.")
        except Exception as e:
            print(e)
            merchantobj = MerchantCategory.objects.get(merchant='default')
    
    return merchantobj      
        
        
        

def savefile(data):
    
    print("saving data")
    for _, row in data.iterrows():
        try:
            
            merchantobj = AssignCategoryAI(row)
            
            _, created = Expenses.objects.get_or_create(
                                txn_date=row['value_date'],
                                desc=row['desc'],
                                cheque_no=row['cheque_no'],
                                txn_amount=row['amount'],
                                balance=row['balance'],
                                merchant=row['user'],  # Exclude merchantobject here
                                defaults={'merchantobject': merchantobj}  # Set merchantobject only if a new record is created
                            )
            if created:
                print("A new expense record was created.")
            else:
                print("The expense record already exists.")
        except Exception as e:
            print(f"Error saving row: {row}, Error: {e}")
    print("file data is saved.")

def processfile(file):
    
    print("processing file: ",file)
    columns = ['txn_date','value_date','desc','cheque_no','debit','credit','balance']
    data = pd.read_excel(file,header=None,skiprows=range(21),names=columns,parse_dates=['value_date','txn_date'])
    data = data[data['desc'].notnull()]
    
    data['value_date'] = pd.to_datetime(data['value_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    data['txn_date'] = pd.to_datetime(data['txn_date'], errors='coerce')
    
    data['user'] = data['desc'].apply(lambda x: x.split('/')[3].lower().strip() if 'transfer' in x.lower() and len(x.split('/'))>3 else x)
    
    data['cheque_no'] = data['cheque_no'].apply(
        lambda x: next((word for word in x.split() if word.isdigit()), None) if pd.notnull(x) else None
    )
    
    data['debit'] = pd.to_numeric(data['debit'], errors='coerce')
    data['credit'] = pd.to_numeric(data['credit'], errors='coerce')
    
    data['amount'] = data.apply(
        lambda row: -pd.to_numeric(str(row['debit']).replace(',', ''), errors='coerce') 
                            if pd.notnull(row['debit']) 
                            else pd.to_numeric(str(row['credit']).replace(',', ''), errors='coerce'),
                            axis=1
    )
    
    data['balance'] = data['balance'].apply(
        lambda x: pd.to_numeric(str(x).replace(',',''),errors='coerce'))
    
    
    
    savefile(data)
    
    
    