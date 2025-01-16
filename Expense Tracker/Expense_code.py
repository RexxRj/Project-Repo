import pandas as pd

category_dict = {
    'food':['swiggy','zomato','foodpanda','dominos','kfc','mcdonalds','burger king','pizza hut'],
    'grocery':['big basket','grofers','d mart','reliance fresh','more','spencers','grocery'],
    'transport':['ola','uber','ola auto','uber auto','ola outstation','uber outstation','ola rental','uber rental','ola bike','uber bike','ola share','uber share','ola micro','uber micro','ola mini','uber mini','ola prime','uber prime','ola lux','uber lux','ola auto','uber auto','ola rental','uber rental','ola bike','uber bike','ola share','uber share','ola micro','uber micro','ola mini','uber mini','ola prime','uber prime','ola lux','uber lux','ola auto','uber auto','ola rental','uber rental','ola bike','uber bike','ola share','uber share','ola micro','uber micro','ola mini','uber mini','ola prime','uber prime','ola lux','uber lux','ola auto','uber auto','ola rental','uber rental','ola bike','uber bike','ola share','uber share','ola micro','uber micro','ola mini','uber mini','ola prime','uber prime','ola lux','uber lux','ola auto','uber auto','ola rental','uber rental','ola bike','uber bike','ola share','uber share','ola micro','uber micro','ola mini','uber mini','ola prime','uber prime','ola lux','uber lux','ola auto','uber auto','ola rental','uber rental','ola bike','uber bike','ola share','uber share','ola micro','uber micro','ola mini','uber mini','ola prime','uber prime','ola lux','uber lux','ola auto','uber auto','ola rental','uber rental','ola bike','uber bike','ola share','uber share','ola micro','uber micro','ola mini','uber mini','ola prime','uber prime','ola lux','uber lux'],
    'shopping':['amazon','flipkart','myntra','jabong','snapdeal','club factory','shein','aliexpress','ebay','shopclues','ajio','limeroad','koovs','zara','h&m','forever 21','lifestyle','shoppers stop','central','pantaloons','westside','max','reliance trends','brand factory','big bazaar','fbb','puma','nike','adidas','reebok','asics','decathlon','under armour'],
    'entertainment': ['netflix'],
    'health': ['medlife','1mg','pharmeasy','netmeds','medplus','apollo pharmacy','healthkart','healthmug','healthgenie'],
    'education': ['udemy','coursera','edx','udacity','khan academy','byjus','vedantu','toppr','meritnation','embibe','unacademy','gradeup','adda247','testbook','oliveboard'],
    'investment': ['paytm money','groww','zerodha','upstox','angel broking','icici direct','hdfc securities','kotak securities','axis direct','5paisa','sharekhan','motilal oswal','edelweiss','iifl','sbi cap securities','reliance securities','geojit','karvy','hdfc bank','icici bank','axis bank','sbi bank','kotak bank','idfc first bank','rbl bank','yes bank','indusind bank','bandhan bank','federal bank','canara bank','bank of baroda','bank of india','punjab national bank','union bank','central bank','indian bank','indian overseas bank','uco bank','vijaya bank','allahabad bank','andhra bank','corporation bank','dhanlaxmi bank','idbi bank','karnataka bank','karur vysya bank','lakshmi vilas bank','nainital bank','south indian bank','syndicate bank','uco bank','yes bank','idfc first bank','rbl bank','bandhan bank','federal bank','canara bank','bank of baroda','bank of india','punjab national bank','union bank','central bank','indian bank','indian overseas bank','uco bank','vijaya bank','allahabad bank','andhra bank','corporation bank','dhanlaxmi bank','idbi bank','karnataka bank','karur vysya bank','lakshmi vilas bank','nainital bank','south indian bank','syndicate bank','uco bank','yes bank','idfc first bank','rbl bank','bandhan bank','federal bank','canara bank','bank of baroda','bank of india','punjab national bank','union bank','central bank','indian bank','indian overseas bank','uco bank','vijaya bank','allahabad bank','andhra bank','corporation bank','dhanlaxmi bank','idbi bank','karnataka bank','karur vysya bank','lakshmi vilas bank','nainital bank','south indian bank','syndicate bank','uco bank','yes bank','idfc first bank','rbl bank','bandhan bank','federal bank','canara bank','bank of baroda','bank'],
    'transfer': ['gunjan','kinjal','prahar'],    
    }

reverse_category_dict = {
    keyword: category
    for category, keywords in category_dict.items()
    for keyword in keywords
}    

def category_classifier(row):
    row_lower = row.lower()
    
    # Check each keyword in the row
    for keyword in reverse_category_dict:
        if keyword in row_lower:
            return reverse_category_dict[keyword]
    
    return 'others'

data = pd.read_excel('expense.xlsx',header=20)
data = data[data['Description'].notnull()]
print(data.head(5))

# columns = ['Date','User','Category','Debit','Credit','Balance']

# str1 = data['Description'][0]
# if 'transfer' in str1.lower():
#     print(str1.split('/')[3])

data['User'] = data['Description'].apply(lambda x: x.split('/')[3] if 'transfer' in x.lower() and len(x.split('/'))>3 else x)

data['Category'] = data['Description'].apply(category_classifier)

print(data.head(5))

# print(data[data['Description'].isna()])

#Data Models

#Expense_sheet - Date, User, Category, Debit, Credit, Balance
#category_sheet - Category, User