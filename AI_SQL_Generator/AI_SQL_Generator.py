from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd


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

chunk_size = 10**6  # For example, 1 million rows per chunk
file_path = "D:\Github\Projects\AI_SQL_Generator\sttm.xlsx"

all_sheets = pd.read_excel(file_path, sheet_name=None)
for sheet_name, df in all_sheets.items():
    print(f'Sheet Name: {sheet_name}')
    print(df.head())  # Display the first few rows of each sheet



# for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
#     print(chunk)

# def main(df):
    
#     transformations = []
#     for index, row in df.iterrows():
#         transformations.append(
#             f"For target column '{row['target_column']}', transform '{row['source_column']}' from table '{row['source_table']}' "
#             f"using transformation logic '{row['transformation_logic']}' (source datatype: {row['source_datatype']}, target datatype: {row['target_datatype']})."
#         )