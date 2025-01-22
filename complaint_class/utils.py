#importing all required  packages
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from nltk import word_tokenize
from sklearn.metrics import accuracy_score, precision_score,classification_report, recall_score
import numpy as np

class utilityFunctions:

  def __init__(self):

    pass


  def data_loading_from_database(self,query):

    """
    This function loads data from database by running the given query and returns the data as dataframe.

    : param - query to fetch data from table
    : type - string
    : return - data fetched from the query
    : rtype - pandas dataframe
    """

    try:
      df = self.sqlContext.sql(query)
      df_pandas = df.toPandas() #converting spark dataframe into pandas dataframe

      return df_pandas

    except ConnectionError as conerror:
      print("Error while connecting with database : ", str(conerror))
      raise conerror

    except Exception as e:
      print("Error occured : ", str(e))
      raise e

  def read_csv(self,filePath, encoding=False):
    """
    This function reads csv file at the given path and returns a dataframe
    
    : param - filePath
    : type - string
    : return - data present in the csv
    : rtype - pandas dataframe
    
    """
    try:
      if encoding:
        data = pd.read_csv(filePath)
      else:
        data = pd.read_csv(filePath, encoding='cp1252')
      
      return data
    
    except Exception as e:
      raise e
  

  def find_vocab(self, list_of_sents):#return vocab size
    """
    This function returns the vocab count for the given list
    
    : param - list_closure_sent (list of sentences)
    : type - list
    : return - count of vocab in the sentence, list of vocab in the sentence
    : rtype - int, list
    """
    try:
      vocab_set_closure_filtered=set([word for sent in list_of_sents for word in word_tokenize(sent)])
      return len(vocab_set_closure_filtered) , vocab_set_closure_filtered
    except Exception as e:
      raise e
      
  def create_complaints_with_risk_dataframe(self, data,list_of_sents):
    """
    This function creates data before preprocessing 
    
    : param -  data
    : type - dataframe
    : param -  list_of_sents
    : type - list
    : return - list of sentences with their respective risk classification
    : rtype - dataframe 
    """
    try:
      target=data['Final_Classification'].tolist()
      training_data=pd.DataFrame({'Data':list_of_sents,'Target':target})
      return training_data
    except Exception as e:
      raise e
      
  def sop_classification_mapping(self, df,mapping_dict):
    """
    This function maps new risks to the complaints as defined in the mapping dictionary created on the SOP(Job aids excel)
    
    : param -  data (training data)
    : type - dataframe
    : param -  mapping dict (dictionary with mapping of category and subcategory with their respective risks)
    : type - dictionary
    : return - list of risk classification as per the mapping dictionary 
    : rtype - list
    """
    ## replace spaces in the category names(keys of mapping dict) and change it to lower case
    mapping_dict =  {k.lower().replace(" ",""): {k1.lower().replace(" ","") :v1 for k1, v1 in v.items()} for k,v in mapping_dict.items()}
    
    try:
      SOP_classification = []
      for i in df[["Final_Category","Final_SubCategory"]].values:

        if not (pd.isnull(i[0])):
          cat= i[0].lower().replace(" ","")
          if not (pd.isnull(i[1])):
            subcat = i[1].lower().replace(" ","")
            if cat in mapping_dict.keys():
              if subcat in mapping_dict[cat].keys():
                if len(mapping_dict[cat][subcat])==1:
                  sop_risk =mapping_dict[cat][subcat][0]
                else:
                  sop_risk = ";".join(mapping_dict[cat][subcat])
              else:
                sop_risk ="SubCategory Not Available"
            else:
                sop_risk ="Category Not Available"
            SOP_classification.append(sop_risk)
          else:
            SOP_classification.append("Subcat is None")
        else:
          SOP_classification.append("Cat is None")

      return SOP_classification
    
    except Exception as e:
      print('Error Occurred : ', e)  
      raise e

      
      
  def create_mapping_dict(self,job_aid_excel_path):
    
    """
      This function creates the mapping dictionary with key as Category and SubCategory and their respective risks as the value. 
      These are derived from the Job Aid excel.

      : param -  job_aid_excel_path (path of the job aid(SOP) excel)
      : type - string
      : return - mapping dict (dictionary with mapping of category and subcategory with their respective risks)
      : rtype - dictionary
    
    """
    mapping_dict={}
    
    try:
      #sop_df = pd.read_excel('/dbfs/FileStore/Nlp_sop/PQC_Job_Aid_Risk_Assessment_v7_updated.xlsx')
      sop_df = pd.read_excel(job_aid_excel_path)
    except Exception as e:
      print("Error occured while reading the excel : ", e)
      raise e      
    
    try:
      #### clean sop_df with following steps 
      
      #--Note : theses steps are specific to the excel used for creating mapping dict (PQC_Job_Aid_Risk_Assessment_v7_updated.xlsx), might need to be edited for new excel
      
      sop_df.dropna(how='all',inplace=True)
      sop_df["Risk Classification"].fillna("High",inplace=True)
      sop_df.isna().sum()
      sop_df.loc[sop_df["Category"] == "Device  (Note: prefilled syringe, auto-injector)", "Category"] = "Device"
      sop_df.loc[sop_df["Category"] == "Primary Container/ Closure\n\nNote: non-device product (e.g., bottle, vial, ampule, blister)","Category"] = "Primary Container/ Closure"
    except Exception as e:
      print("Error occured while cleaning the dataframe : ", e)
      raise e 
        
    try:
      for cat in sop_df.Category.unique():
        temp={}
        for subcat in (sop_df["Subcategory"][sop_df.Category==cat].unique()):
          temp[subcat] =sop_df["Risk Classification"][(sop_df.Category==cat) & (sop_df.Subcategory==subcat)].to_list()
        mapping_dict[cat] = temp      
        
      return mapping_dict
    except Exception as e:
      print("Error occured while creating mapping dictionary : ", e)
      raise e 
     
    

# COMMAND ----------

# DBTITLE 1,This class contains all the functions we are using for dataframe operations.
#data filtering on the basis of awareness date and year

class DataframeOperations:

  def filterting_data_using_awareness_date(self,dataframe, openDate, closeDate, training_flag=False):
    """
    This function filters data on the basis of awareness date we are only using data having awareness date greater than
    2021 and less than 2022-10-14
     
    : param - dataframe
    : type - pandas dataframe
    : param - openDate (date after (>=) which have to filter data : format "yyyy-mm-dd" : default= "2021" (for training))
    : type -string
    : param - closeDate (Date till(<) which have to filter data : format "yyyy-mm-dd" : default= 2022-10-14"")
    : type -string
    : return - filtered dataframe
    : rtype - pandas dataframe
    
    """
    try:
      if openDate is None and closeDate is not None:
        dataframe=dataframe[(pd.to_datetime(dataframe['Awareness_Date']))< closeDate]
      elif closeDate is None and openDate is not None:
        dataframe=dataframe[(pd.to_datetime(dataframe['Awareness_Date']))>=openDate]
      elif openDate is not None and closeDate is not None:
        dataframe=dataframe[((pd.to_datetime(dataframe['Awareness_Date']))>=openDate) & ((pd.to_datetime(dataframe['Awareness_Date']))< closeDate)]
        
      #returning only those complaints which have been closed on the basis of is_closed filter
      if training_flag:#will do this filtering only for training 
          data = dataframe[dataframe['is_closed']=='1']
          if len(data) < 1:
                raise Exception("None of the tickets are closed")
          else:
              return data
      else:
        return dataframe
    except Exception as e:
      raise e 
      
  def replace_na_value(self,dataframe,col_name="Final_Classification", value_to_fill="NA"):
    """
    This function replaces na values for the given column with the value provided to replace it with. 
    Specially created to fill na values in Final Classification column with "NA".
    
    : param - dataframe
    : type - pandas dataframe
    : param - col_name (default= "Final_Classification")
    : type - list 
    : param - value_to_fill (default ="NA")
    : type - string  
    : return - dataframe after replacing nan value 
    : rtype - pandas dataframe
    """
    try:
     
      dataframe[col_name]=dataframe[col_name].fillna(value_to_fill)
      
      return  dataframe
    except Exception as e:
      raise e 


  def removing_na_value(self,dataframe,col_names):#remove na value for given columns
    """
    This function removes na values for the given columns
    : param - dataframe
    : type - pandas dataframe
    : param - col_names
    : type - list 
    : return - dataframe after remoing nan value 
    : rtype - pandas dataframe
    """
    try:
      #dataframe=dataframe.fillna(value=np.nan)
 
      dataframe=dataframe.dropna(subset=col_names)
      return dataframe
    except Exception as e:
      raise e

# COMMAND ----------

# DBTITLE 1,This class contains all the required functions for embedding process.
class embeddingPipeline:
  
  def __init__(self,EmbeddingModelName):
    
    self.EmbeddingModelName=EmbeddingModelName
    
  def loadEmbeddingModel(self):
    
    try:
      
      return SentenceTransformer(self.EmbeddingModelName)
    
    except Exception as e:
      raise e
    
    
  def sentence_transformer_sent_embd(self,list_of_sents):
    """
    Function generates sentence embeddings for training using sentence transformer model 
    : param - list_of_sents
    : type - list 
    : return - list of embeddings for sentences 
    : rtype - list 
    """
    try:
      model= self.loadEmbeddingModel()
      sents_embeddings=[]
      count=0
      for index, sent in enumerate(list_of_sents):
        embedding = model.encode(sent)
        sents_embeddings.append(embedding)
      return sents_embeddings
    except Exception as e:
      raise e

# COMMAND ----------

def calculate_final_metrics(data):

  metrics_df = pd.DataFrame()
  total_complaints = data.shape[0]
  data = data[data["Predicted_Risk"] != 'Complaint is not in english language']
  total_predicted_complaints = data.shape[0]
  data["Actual_Risk_Label"] = [1 if x =='LOW' else 0 for x in data["Actual_Risk"]]
  data["Predicted_Risk_Label"] = [1 if x == 'LOW' else 0 for x in data["Predicted_Risk"]]
  print(classification_report(data["Actual_Risk_Label"], data["Predicted_Risk_Label"]))
  # print(precision_score(data["Actual_Risk_Label"], data["Predicted_Risk_Label"]))
  # print(recall_score(data["Actual_Risk_Label"], data["Predicted_Risk_Label"]))
  # print(accuracy_score(data["Actual_Risk_Label"], data["Predicted_Risk_Label"]))
  precision = precision_score(data["Actual_Risk_Label"], data["Predicted_Risk_Label"])
  recall = recall_score(data["Actual_Risk_Label"], data["Predicted_Risk_Label"])
  accuracy  = accuracy_score(data["Actual_Risk_Label"], data["Predicted_Risk_Label"])
  correct_predicted_low_complaints = int(data[(data["Actual_Risk_Label"]==1) & (data["Predicted_Risk_Label"]==1)].shape[0])
  wrong_predicted_low_complaints = int(data[(data["Predicted_Risk_Label"] == 1)].shape[0]) - correct_predicted_low_complaints

  metrics = {
    "Total_Complaints": total_complaints,
    "Total_Complaints_With_Predictions": total_predicted_complaints,
    "Correct Predicted Low": correct_predicted_low_complaints,
    "Wrong Prediction Low": wrong_predicted_low_complaints,
    "Precision_score": np.round(precision, decimals=2),
    "Recall_Score":  np.round(recall,decimals=2),
    "Accuracy_Score": np.round(accuracy,decimals=2),
                }
  return pd.DataFrame([metrics])