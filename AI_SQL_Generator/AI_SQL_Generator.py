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
csv_file = "D:/projects/New_Project/sttm.csv"


for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
    print(chunk)