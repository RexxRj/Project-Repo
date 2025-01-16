from .models import Expenses, MerchantCategory
import pandas as pd

def savefile(data):
    
    print("saving data")
    for _, row in data.iterrows():
        try:
            
            merchantobj = MerchantCategory.objects.filter(merchant=row['user'].lower().strip()).first()
            
            if not merchantobj:
                merchantobj = MerchantCategory.objects.get(merchant='default')
            
            Expenses.objects.create(
                txn_date = row['value_date'],
                desc = row['desc'],
                cheque_no=row['cheque_no'],
                            txn_amount=row['amount'],
                            balance=row['balance'],
                            merchant=row['user'],
                            merchantobject=merchantobj
            )
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
    
    data['user'] = data['desc'].apply(lambda x: x.split('/')[3] if 'transfer' in x.lower() and len(x.split('/'))>3 else x)
    
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
    
    
    