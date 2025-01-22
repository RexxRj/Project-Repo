# Databricks notebook source
#!pip install pycld2==0.41

#importing all required  packages
#import pycld2 as cld2
import regex
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from langdetect import detect
import numpy as np

# COMMAND ----------

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

# COMMAND ----------

## name of class TrainingData changed to preprocessing_for_training,

class preprocessing:
  
  def __init__(self,dataframe,utility_function_obj):
    self.dataframe = dataframe
    self.utility=utility_function_obj
    self.vocab=None
    self.vocab_len=None
    self.training_data=None
    self.re_bad_chars= regex.compile(r"[\p{Cc}\p{Cs}]+")
    
    
  def remove_bad_chars(self,text):
    """
    This function removes all characters defined in the regex pattern from the given text to use in language detection model.
    
    : param - RE_BAD_CHARS
    : type - regex
    : param - text
    : type - str
    : return - text with characters defined in regex substituted with whitespace
    : rtype - str
    """
    try:
      return self.re_bad_chars.sub("", text)
    
    except Exception as e:
      raise e

      
  def different_lang_detection(self, data, columnName='Complaint_Description'):
    
    """
    This function detects language present in the complaints and returns (sentence and it's index) of different languages.
    
    : param - data
    : type - dataframe
    : return - two lists of indexes of sentences with mutilple languages and other languages
    : rtype - list
    """
    
    try:
      multi_lan=[] 
      other_lan=[]
      english_language_index=[]
      multi_lang_index=[]
      non_english_language_index=[]
      english_language_list=[]
      non_english_language_list=[]
      for index,sent in enumerate(data[columnName].tolist()):
        sent=self.remove_bad_chars(sent)
        
        # _, _, _, detected_language = cld2.detect(sent,returnVectors=True)
        #
        #
        # if len(list(detected_language))==1:
        #   if list(detected_language[0])[2] == 'ENGLISH':
        #
        #     english_language_list.append(sent)
        #     english_language_index.append(index)
        #   else:
        #     non_english_language_list.append((index ,"Complaint is not in english language"))#this will be used for inference
        #     non_english_language_index.append(index)
        # else:
        #   multi_lan.append(sent)
        #   multi_lang_index.append(index)
        #   english_language_list.append(sent)
        #   english_language_index.append(index)

        # return multi_lang_index , non_english_language_index , non_english_language_list , english_language_list , english_language_index

        if detect(sent)== "en":
          english_language_list.append(sent)
          english_language_index.append(index)
        else:
            non_english_language_list.append((index ,"Complaint is not in english language"))#this will be used for inference
            non_english_language_index.append(index)
          
      return non_english_language_index , non_english_language_list , english_language_list , english_language_index
    
    except Exception as e:
      #print('Error ocurred : ', str(e))
      raise e


  def sent_preprocessing(self, list_closure_sent,flag=False,english_language_index=None): 
    
    """
    Sentence preprocessing function removes all irrelevant characters from sentence and checks if words in sentence are characters and english characters only,
    complaints with non english words are not added in the final list and their indexes are returned to be dropped.
    flag helps in inference phase if True means inference else training 
    english language index helps to append original index of the non-english sents which have not been detected as non english after language 
    detection method
    
    : param - list_closure_sent (list of sentences)
    : type - list
    : param - flag
    : type - boolean
    : param - english_language_index
    : type - list 
    : return - list of sentences after removing irrelevant characters and list of indexes of irrelevant complaints
    : rtype - list
    """
    
    try:

      relevant_complaints_list=[]
      index_irrelevant_complaints=[]
      for index,single_sent in enumerate(list_closure_sent):
        
        tmp_list=[]
        single_sent = single_sent.replace('\r',' ').replace('\n',' ').replace('.',' ')\
                                  .replace(':',' ').replace("?",' ').replace("\'",'').replace(',',' ').replace("\"",'').replace(';',' ')
        
        for word in word_tokenize(single_sent):

          if word.isalpha() and word.isascii():
            tmp_list.append(word.lower())
        
      ##--adding below check as after preprocessing for some irrelevant complaints, "tmp_list" is left with one character or no character(blank list gets appended in final list)
        if len(tmp_list)>1: 
          relevant_complaints_list.append(" ".join(tmp_list))
        else:
          if flag:
            index_irrelevant_complaints.append(english_language_index[index])
          else:
            index_irrelevant_complaints.append(index)
          
      return relevant_complaints_list,index_irrelevant_complaints
    
    except Exception as e:
      print('Error Occurred: ',e)
      raise e
  
  ## name of function training_data_without_embd changed to preprocessing_training_data
  def preprocessing_training_data(self,mapping_dict):
    """
    This function performs preprocessing on the training data by removing different languages and sentence preprocessing.
      : param - dataframe
      : type - pandas dataframe 
      : return - return training data with processed complaints text and sop classification  
      : rtype - pandas dataframe
    """
    try:
      #multi_lang_index , other_lang_index,_,_,_ = self.different_lang_detection(self.dataframe)
      non_english_language_index, non_english_language_list, english_language_list, english_language_index = self.different_lang_detection(self.dataframe)
    except Exception as e:
      raise e
    
    try:
      english_language_data=self.dataframe.drop(self.dataframe.index[non_english_language_index],axis=0)#dropping all the other lang indices
      english_language_data.reset_index(inplace=True)
      list_of_sents=english_language_data['Complaint_Description'].tolist()
      list_of_sents , list_of_indices_to_rem=self.sent_preprocessing(list_of_sents)#sentence preprocessing
    except Exception as e:
      raise e
    
    try:
      english_language_data=english_language_data.drop(english_language_data.index[list_of_indices_to_rem],axis=0)
      english_language_data.reset_index(inplace=True)
      #self.vocab_len , self.vocab = self.utility.find_vocab(list_of_sents)
      training_data=self.utility.create_complaints_with_risk_dataframe(english_language_data,list_of_sents)
    except Exception as e:
      raise e
    
    try:
      training_data['Pr_Id']=english_language_data['pr_id']
      english_language_data=english_language_data.fillna(value=np.nan)
      training_data['SOP_classification']=self.utility.sop_classification_mapping(english_language_data,mapping_dict)
      training_data['Initial_classification']=english_language_data['Initial_Classification']
      training_data['Final_Subcategory']=english_language_data['Final_SubCategory']
      #training_data['Initial_Subcategory']=english_language_data['Initial_SubCategory']
      self.training_data=training_data  
      return training_data
    
    except Exception as e:
      raise e

# COMMAND ----------