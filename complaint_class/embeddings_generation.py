# Databricks notebook source
# importing all required  packages
import pandas as pd
import numpy as np
from utils import utilityFunctions, DataframeOperations, embeddingPipeline
from preprocessing import preprocessing
import regex
from config import mapping_dict, EMBEDDING_MODEL, RE_BAD_CHARS, embedding_path, data_path

# COMMAND ----------

utilityFunctions_obj = utilityFunctions()
dfops_obj = DataframeOperations()
embed_obj = embeddingPipeline(EMBEDDING_MODEL)


# COMMAND ----------

def embedding_generation_for_training(embedding_saving_path=None, data_path=None, mapping_dict=None):
    try:

        # data = utilityFunctions_obj.data_loading_from_database(queryToFetchData)
        data = utilityFunctions_obj.read_csv(filePath=data_path)

        # filter data from the whole dataset based on the awareness date
        # data = dfops_obj.filterting_data_using_awareness_date(data,openDate,closeDate,training_flag=True)
        print('data shape', data.shape)
        # removing na values from "Complaint Description" column
        data = dfops_obj.removing_na_value(data, ['Complaint_Description'])

        # replace/fill na values from "Final Classification" column as "NA"
        data = dfops_obj.replace_na_value(data)
        # replace/fill na values from "Initial Classification" column as "NA"
        data = dfops_obj.replace_na_value(data, col_name="Initial_Classification")
        # initilize preprocessing for training class
        preprocessing_obj = preprocessing(data, utilityFunctions_obj)
        # preprocessing the training data
        preprocessed_data = preprocessing_obj.preprocessing_training_data(mapping_dict)
        # generate embeddings on the Data column (text data from preprocessed complaints)
        sent_emb = embed_obj.sentence_transformer_sent_embd(preprocessed_data['Data'])

        # creating dataframe with the respective embeddings of the cleaned complaints data
        sent_emb_df = pd.DataFrame(sent_emb)
        sent_emb_df['Pr_Id'] = preprocessed_data['Pr_Id']
        sent_emb_df['Original'] = preprocessed_data['Data']
        sent_emb_df['Target'] = preprocessed_data['Target']
        sent_emb_df['SOP_classification'] = preprocessed_data['SOP_classification']
        sent_emb_df['Initial_classification'] = preprocessed_data['Initial_classification']
        sent_emb_df['Final_Subcategory'] = preprocessed_data['Final_Subcategory']

        # save the embeddings as csv
        print('----------------------saving embedding------------------------')
        sent_emb_df.to_csv(embedding_saving_path, index=False)
        print('---------------------------embeddings saved-------------------')
        # raise 'Exception raised'
        return sent_emb_df

    except Exception as e:
        print('Exception while generating embeddings :', e)
        raise e


embedding_generation_for_training(embedding_saving_path=embedding_path, data_path=data_path, mapping_dict=mapping_dict)
