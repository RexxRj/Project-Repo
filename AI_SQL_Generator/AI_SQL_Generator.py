from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from langchain import LLMChain
import pandas as pd
# from langchain.schema import Message


  # For example, 1 million rows per chunk

# all_sheets = pd.read_excel(file_path, sheet_name=None)

# for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
#     print(chunk)

# def main(df):
    
#     transformations = []
#     for index, row in df.iterrows():
#         transformations.append(
#             f"for target column '{row['target_column']}', transform '{row['source_column']}' from table '{row['source_table']}' "
#             f"using transformation logic '{row['transformation_logic']}' (source datatype: {row['source_datatype']}, target datatype: {row['target_datatype']})."
#         )



load_dotenv()

API_KEY = os.getenv("API_KEY")
    
genai.configure(api_key=API_KEY)
    
os.environ["GOOGLE_API_KEY"] = API_KEY
    
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)
    
prompt = {
        "role": "system",
        "content": """You are a intelligent SQL Query Generator. 
        You take the mapping of source and target along with each column information and other joining conditions, aggregations etc. 
        to generate any kind of query.
        Return only the select query as output."""   
        }
    
    
file_path = os.getenv("file_path")
chunk_size = 10**6
    
tgt_ovr_df = pd.read_excel(file_path, sheet_name = "Target_Overview")
    
assert tgt_ovr_df.empty == False, "No Target Information is given."

tgt_schema = tgt_ovr_df.loc[0,'target_schema']
tgt_tbl = tgt_ovr_df.loc[0,'target_table']
main_src_schema = tgt_ovr_df.loc[0,'main_src_schema']
main_src_tbl = tgt_ovr_df.loc[0,'main_src_table']
sql_ovrv = tgt_ovr_df.loc[0,'sql_overview']
pre_prmpt_ovrv = tgt_ovr_df.loc[0,'pre_prompt']
post_prmpt_ovrv = tgt_ovr_df.loc[0,'post_prompt']
        
assert pd.notna(tgt_schema), "target_schema is not given"
assert pd.notna(tgt_tbl), "target_table is not given"
assert pd.notna(main_src_schema), "main_src_schema is not given"
assert pd.notna(main_src_tbl), "main_src_tbl is not given"
        
if(sql_ovrv == None or pd.isna(sql_ovrv)):
    sql_ovrv = "Generate a SQL Query."
if(pre_prmpt_ovrv == None or pd.isna(pre_prmpt_ovrv)):
    pre_prmpt_ovrv = ""   
if(post_prmpt_ovrv == None or pd.isna(post_prmpt_ovrv) ):
    post_prmpt_ovrv = ""
        
    
print(f"Target Schema: {tgt_schema}")
print(f"Target Table: {tgt_tbl}")
print(f"Source Schema: {main_src_schema}")
print(f"Source Table: {main_src_tbl}")
print(f"SQL Overview: {sql_ovrv}")
print(f"Pre-Prompt Overview: {pre_prmpt_ovrv}")
print(f"Post-Prompt Overview: {post_prmpt_ovrv}")

            
message1 = {"role": "user",
            "content": """ You have been given the following variables to define the overall structure of the query.\n
            These variables should be always kept consistent while creating the query. Any nan,None,null input should be treated as no input given 
            and default values should be used instead.\n
            Target_Table = {tgt_tbl}\n
            Target_Schema = {tgt_schema}\n
            All tables should be in the format Target_schema.Target_Table.\n
            Keep in mind these overview of the query always:\n
            {sql_overview}\n
            {pre_prompt_overview}\n"""

            }
        
print(message1)
        
tgt_col_df = pd.read_excel(file_path, sheet_name = "Target_Mapping")
        
transformations = []
for index, row in tgt_col_df.iterrows():
    transformations.append(
        f"\n{index+1}. For target column '{row['target_column']}', transform '{row['source_column']}' from table '{row['source_schema']}'.'{row['source_table']}' "
        f"using transformation logic '{row['transformation_logic']}' (source datatype: {row['source_datatype']}, target datatype: {row['target_datatype']})."
    )
        
print(transformations)
    
ref_ovr_df = pd.read_excel(file_path, sheet_name = "Reference_Overview")
if ref_ovr_df.empty:
    print("ref_ovr_df is empty.")
    ref_pre_prompt = None
    ref_post_prompt = None
    filter_conditions = None
else:
    ref_pre_prompt = ref_ovr_df.loc[0,'pre_prompt_ref']
    ref_post_prompt = ref_ovr_df.loc[0,'post_prompt_ref']
    filter_conditions = ref_ovr_df.loc[0,'filter_conditions']
    
if(ref_pre_prompt == None or pd.isna(ref_pre_prompt)):
    ref_pre_prompt = ""
if(ref_post_prompt == None or pd.isna(ref_post_prompt)):
    ref_post_prompt = ""   
if(filter_conditions == None or pd.isna(filter_conditions)):
    filter_conditions = ""
    
print(ref_pre_prompt,ref_post_prompt,filter_conditions)
    
ref_col_df = pd.read_excel(file_path, sheet_name = "Reference_Mapping")
    
ref_check = ref_col_df.empty
ref_transformations = ["{ref_pre_prompt}"]
if ref_check == False:
    ref_transformations.append("\nMake the reference joins based on the conditions given. Treat any nan, NA, None etc. values as no condition given."
                            "\nIf no joining condition or target joining column given, it means we are just pulling the column from reference table "
                            "in main query without having it in joining clause.\n"
                            )
    for index, row in ref_col_df.iterrows():
        ref_transformations.append(
        f"\n{index+1}. For column '{row['ref_col_nm']}' (dataype: '{row['ref_datatype']}' coming from reference table '{row['ref_schema']}'.'{row['ref_table']}') "
        f"using transformation logic '{row['transformations']}' "
        f"joining with table '{row['join_schema']}'.'{row['join_table']}' join type '{row['join_type']}' on column '{row['tgt_join_col']}' "
        f"conditions '{row['conditions']}' "
            
        )
    
print(ref_transformations)
    
message2 = {"role":"user",
                "content":"""After creating the reference joins and the structure of the query, adjust the query according to these conditions:
                filter_condition: {filter_conditions}
                {ref_post_prompt}"""  
                }
    
message3 = {"role":"user",
                "content":"{post_prmpt_ovrv}"}

transformations = '\n'.join(transformations)
ref_transformations_str = '\n'.join(ref_transformations)

#print(type(message3),type(message3['role']),type(message3['content']),message3['role'])

# messages = [
#     Message(role=prompt['role'], content=prompt['content']),
#     Message(role=message1['role'], content=message1['content']),
#     Message(role="user", content=transformations),
#     Message(role="user", content=ref_transformations),
#     Message(role=message2['role'], content=message2['content']),
#     Message(role=message3['role'], content=message3['content']),
# ]

# chat_prompt = ChatPromptTemplate.from_messages(messages)


chat_prompt = ChatPromptTemplate.from_messages([
(prompt['role'], prompt['content']),
(message1['role'], message1['content']),
("user", transformations),
("user",ref_transformations),
( message2['role'], message2['content']),
( message3['role'], message3['content'])
])
    
input_data = {
        
    "tgt_tbl":tgt_tbl,
    "tgt_schema":tgt_schema,
    "sql_overview":sql_ovrv,
    "pre_prompt_overview":pre_prmpt_ovrv,
    "ref_pre_prompt":ref_pre_prompt,
    "filter_conditions":filter_conditions,
    "ref_post_prompt":ref_post_prompt,
    "post_prmpt_ovrv":post_prmpt_ovrv
    }
    
sql_chain = LLMChain(prompt=chat_prompt, llm=llm)
    
generated_sql = sql_chain.run(input_data)
    
print(generated_sql)



    
