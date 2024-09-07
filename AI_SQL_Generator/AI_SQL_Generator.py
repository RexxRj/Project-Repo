from re import I
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd
from pandas.io import sql

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

def main():
    try:
    
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
    
        prompt = [
            {
                "role": "system",
                "content": "You are a intelligent SQL Query Generator. You take the mapping of source and target along with each column information and other joining conditions, aggregations etc. to generate any kind of query."   
                }
            ]
    
        file_path = os.getenv("file_path")
        chunk_size = 10**6
    
        tgt_ovr_df = pd.read_excel(file_path, sheet_name = "Target_Overview")

        tgt_schema = tgt_ovr_df.loc[0,'target_schema']
        tgt_tbl = tgt_ovr_df.loc[0,'target_table']
        sql_ovrv = tgt_ovr_df.loc[0,'sql_overview']
        pre_prmpt_ovrv = tgt_ovr_df.loc[0,'pre_prompt']
        post_prmpt_ovrv = tgt_ovr_df.loc[0,'post_prompt']
        
        print(f"Target Schema: {tgt_schema}")
        print(f"Target Table: {tgt_tbl}")
        print(f"SQL Overview: {sql_ovrv}")
        print(f"Pre-Prompt Overview: {pre_prmpt_ovrv}")
        print(f"Post-Prompt Overview: {post_prmpt_ovrv}")
        
        assert pd.notna(tgt_schema), "target_schema is not given"
        assert pd.notna(tgt_tbl), "target_table is not given"
        
        if(sql_ovrv == None):
            sql_ovrv = "Generate a SQL Query."
        if(pre_prmpt_ovrv == None):
            pre_prmpt_ovrv = "Generate the SQL Query."   
        if(post_prmpt_ovrv == None):
            post_prmpt_ovrv = "Generate the SQL Query."
            
        message1 = {"role": "user",
                    "content": """ You have been given the following variables to define the overall structure of the query.
                    These variables should be always kept consistent while creating the query.
                    Target_Table = {tgt_tbl}
                    Target_Schema = {tgt_schema}
                    All tables should be in the format Target_schema.Target_Table.
                    Keep in mind these overview of the query always:
                    {sql_overview}                
                    """
                    }
        
        print(message1)
        
        tgt_col_df = pd.read_excel(file_path, sheet_name = "Target_Mapping")
        # TODO
        transformations = []
        for index, row in tgt_col_df.iterrows():
            transformations.append(
                f"{index+1}. For target column '{row['target_column']}', transform '{row['source_column']}' from table '{row['source_table']}' with schema '{row['source_schema']}'"
                f"using transformation logic '{row['transformation_logic']}' (source datatype: {row['source_datatype']}, target datatype: {row['target_datatype']})."
            )
        
        print(transformations)


    except Exception as main_err:
        raise main_err
    
main()