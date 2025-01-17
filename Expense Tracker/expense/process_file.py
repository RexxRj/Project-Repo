from .models import Expenses, MerchantCategory
import pandas as pd
# import google.generativeai as genai
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain import LLMChain
# from dotenv import load_dotenv


# load_dotenv()

# API_KEY = os.getenv("API_KEY")
    
# genai.configure(api_key=API_KEY)
    
# os.environ["GOOGLE_API_KEY"] = API_KEY
    
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2
# )

def AssignCategoryAI(row):
    merchant = row['user'].lower().strip()
    merchantobj = MerchantCategory.objects.filter(merchant=merchant).first()
    
    
    if not merchantobj:
        
        # try:
        
        #     categories = MerchantCategory.objects.values('category').distinct()
        #     prompt = {
        #     "role": "system",
        #     "content": """You are a intelligent category assigning agent.
        #     You take merchant name which can be any upi merchant transaction like 
        #     food transactions, travel transactions, friends transactions etc.
        #     You will assign correct category to the transaction from a list that is provided to you.
        #     You will only return the category and nothing else.
        #     """   
        #     }
            
        #     print(prompt)
            
        #     message1 = {"role": "user",
        #         "content": f""" 
        #         Merchant Name: {merchant},
        #         Categories: {[x['category'] for x in categories]},
        #         Please provide a one category for this merchant
        #         """

        #         }
            
        #     print(message1)
            
        #     chat_prompt = ChatPromptTemplate.from_messages([
        #     (prompt['role'], prompt['content']),
        #     (message1['role'], message1['content'])
        #     ])
            
        #     prompt_chain = LLMChain(prompt=chat_prompt, llm=llm)
            
        #     print("running")
            
        #     category = prompt_chain.run({})
            
        #     print("category: ",category)
            
            
        #     merchantobj,created = MerchantCategory.objects.get_or_create(
        #             merchant=merchant,
        #             category = category
        #         )
            
        #     print("done")
        # except Exception as e:
        #     print(e)
        merchantobj = MerchantCategory.objects.get(merchant='default')
    
    return merchantobj      
        
        
        

def savefile(data):
    
    print("saving data")
    for _, row in data.iterrows():
        try:
            
            merchantobj = AssignCategoryAI(row)
            
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
    
    
    