# Databricks notebook source
from time import time
import pandas as pd
import os
from preprocessing import preprocessing
import numpy as np
from utils import utilityFunctions
from utils import embeddingPipeline
from utils import DataframeOperations
import pickle

class Prediction():
  
  def __init__(self,utilityFunctionsObj,embeddingPipeline,PREDICTION_EMBEDDING_PATH=None):
    self.utility=utilityFunctionsObj
    self.embeddingPipeline=embeddingPipeline
    self.PREDICTION_EMBEDDING_PATH=PREDICTION_EMBEDDING_PATH
    
    
  def data_preprocessing_for_inference(self,dataframe):
    """
    Function creates data for testing  by performing all needed steps before feeding the data into the model for inference
    : param - data
    : type - list
    : param - embedding_model
    : type - sentence transformer's object
    : return - embedded data , non-english language data and english language data
    : rtype - list
    """


      #process only english sents
    try:
      print('from inference',dataframe.shape)
      preprocessingObj=preprocessing(dataframe,self.utility)
      non_english_language_index, non_english_language_list, english_language_list, english_language_index = preprocessingObj.different_lang_detection(dataframe)
      print('after preprocessing : ')
      relevant_data,irrelevant_complaints_index=preprocessingObj.sent_preprocessing(english_language_list,flag=True,\
                                                                                            english_language_index=english_language_index)
      
      if len(relevant_data) < 1: #if we do not get any relevant complaint to avoid error we return
        return pd.DataFrame(),non_english_language_list,english_language_index,dataframe,relevant_data,irrelevant_complaints_index
      
      relevant_data_embedding =self.embeddingPipeline.sentence_transformer_sent_embd(relevant_data)
      print('----------------------saving embedding------------------------')
      df_embedding=pd.DataFrame(relevant_data_embedding)
      dataframe=dataframe.drop(dataframe.index[irrelevant_complaints_index + non_english_language_index],axis=0)
      dataframe.reset_index(inplace=True)
      df_embedding['Pr_Id']=dataframe['Pr_id'].tolist()

      #---------------------adding new embeddings with old embeddings-------------
      # if os.path.exists(self.PREDICTION_EMBEDDING_PATH):
      #   old_embedding = pd.read_csv(self.PREDICTION_EMBEDDING_PATH)
      # else:
      #   print('if path does not exist')
      #   old_embedding = pd.DataFrame()
      # print('old embedding shape',old_embedding.shape)
      # print('data embedding shape',df_embedding.shape)
      # print(old_embedding.columns)
      # print(df_embedding.columns)
      # df_embedding.to_csv("/dbfs/FileStore/nlpcc/prediction_complaints_new_embedding_iteration.csv",index=False)#saving local embedding for every run
      #
      # df_embedding = pd.read_csv("/dbfs/FileStore/nlpcc/prediction_complaints_new_embedding_iteration.csv")
      # #we will read from csv again to do the merging otherwise we can not do that because column names type are different
      # df_embedding = pd.concat([old_embedding,df_embedding],axis = 0)
      #
      # #--------------------------------------------------------------------
      # #removing duplicate complaints to maintain the memory size
      # df_embedding=df_embedding.drop_duplicates(subset=['Pr_Id'])

      df_embedding.to_csv(self.PREDICTION_EMBEDDING_PATH,index=False) #global embeddings files after merging all embedding 
      #on different run
      print('combine embedding shape',df_embedding.shape)
      print('---------------------------embeddings saved-------------------')
      
      return relevant_data_embedding,non_english_language_list,english_language_index,dataframe,relevant_data,irrelevant_complaints_index
    except Exception as e:
      raise e
      
  def eval_model_testing(self,X_test,model):
    """
    This function evaluates the model using  X_test->embedded complaints

    : param - X_test
    : type - list
    : param - model
    : type - model object(e.g trained model Logistic, SVM etc )
    : param - modelname
    : type - string 
    : return - predicted target classes 
    : rtype - list
    """
    try:
    
      y_pred= model.predict(X_test)
      return y_pred
    except Exception as e:
      raise e
      
  def predicted_result_into_risk_category(self,complete_final_prediction,low=None):
    try:
        predicted_result=[]
        for risk in complete_final_prediction:
            if risk==1:#low
                predicted_result.append(low)
            elif risk==0:
                predicted_result.append('OTHER')
            else:
                predicted_result.append(risk)

        return predicted_result
    except Exception as e:
        raise e
  
  def subcategory_prediction(self,data,model_subcat,threshold=0.85):
    """
    This function will do the classification for medium risk using low risk predictions
    : param - data (dataframe of embedding with low risk classification)
    : type - dataframe
    : param - model_subcat
    : type - trained models object
    : return - data (dataframe with subcategory classification)
    : rtype - pandas dataframe
    """
    try:
        
        low_data=data[data['prediction']==1] #filtering low risk 
        other_data=data[data['prediction']==0] #filtering other risk
        low_data_index=low_data.index.tolist()#storing index will use later to combine both data together
        other_data_index=other_data.index.tolist()
        data_for_prediction=low_data.drop(['prediction'],axis=1)#dropping this column so that we can feed word embedding only in our model
        print('low data for subcategory modelling',low_data.shape)
        print('other data from subcategory model',other_data.shape)
        if len(data_for_prediction):
          #added above if  condn (4th-apr-2024), if we have low data then only we process subcat model
          #otherwise subcat model will throw error.
          print('calling subcategory model on low risk complaints',low_data.shape)
          y_pred_prb = model_subcat.predict_proba(data_for_prediction)
          subcat_model_result = [1 if i[1] > threshold else 0 for i in y_pred_prb]
          print('len of the data',len(data),'len of low data index',len(low_data_index),'len of other index',len(other_data_index))
          data['Predicted_SubCategory']=''
          data.loc[low_data_index,'Predicted_SubCategory']=['Lack of Effect' if res==1 else 'OTHER' for res in subcat_model_result]
          #OLD SUBCAT VALEU - LOE
          #appending subcategory model 
        #results
        print('other index list from subcategory modelling',other_data_index)
        data.loc[other_data_index,'Predicted_SubCategory']=['NA' for i in other_data_index]#for other class we use NA
        
        return data

    except Exception as e:
        raise e

  def load_saved_model(self,model_path):
    try:
        with open(model_path, 'rb') as f:
          model = pickle.load(f)

        return model
    except Exception as e:
        raise e

  def model_prediction(self,data,model_sop,model_fc,model_low_ini=None,model_subcategory=None):
    """
    This function generates the results for real time inference
    : param - data
    : type - list
    : param - model_sop , model_fc
    : type - trained models object
    : return - classified data 
    : rtype - pandas dataframe
    """
    try:
      embedding_data ,non_english_complaints,english_language_index , _ , relevant_data,irrelevant_complaints_index= self.data_preprocessing_for_inference(data)
      #--Note -- > in english language index we are also appending multilingual language and those complaints can be handled
      #later using irrelevant_complaints_index 

    except Exception as e:
      raise e

    try:
      if len(embedding_data) < 1:
          #------------------- if do not get any english complaints this block will execute-------------------
          final_output=pd.DataFrame()
          final_output['Complaints']=data['Complaint_Description'] 
          #when complaints are not in english we do not do preprocessing that's why appending data as it is.
          final_output['Preprocessed Complaints']=data['Complaint_Description'].tolist()
          final_output['Predicted_Risk'] = "Complaint is not in english language" #we know that our model will no any prediciton
          #on non-english complaints that's why making prediction like above
          final_output['Predicted_SubCategory']='NA'
          return final_output
      else:
        try:
          y_pred_sop =self.eval_model_testing(embedding_data,model_sop)
          #y_pred_fc =self.eval_model_testing(embedding_data,model_fc)
          y_pred_fc = [1 if i[1] > 0.80 else 0 for i in model_fc.predict_proba(embedding_data)]
          #y_pred_ini =self.eval_model_testing(embedding_data,model_low_ini)
          #y_pred_ini = [1 if i[1] > 0.70 else 0 for i in model_low_ini.predict_proba(embedding_data)] ##checking with threshold on initial model
          #print(len(y_pred_sop),len(y_pred_fc))
        except Exception as e:
          raise e
          
        try:
          final_output=pd.DataFrame()
          final_output['Complaints']=data['Complaint_Description'] 
          
          preprocessed_complaints=list(np.zeros(len(data))) #making a list of same size as input because we will get embeddings and preprocessed 
          #data only for the relevant data but we need to add rest data as well.

          if len(irrelevant_complaints_index):
            for irr_ind in irrelevant_complaints_index: #removing irrelevant indices from english language index (lang detection code)
              english_language_index.remove(irr_ind)
          
          for relevant_ind , relevant_d in zip(english_language_index,relevant_data): #adding relevant processed complaint using index value
            preprocessed_complaints[relevant_ind]=relevant_d
          
          for index , d in enumerate(preprocessed_complaints):
            if d==0:
              preprocessed_complaints[index]=data['Complaint_Description'].tolist()[index] #adding those complaints which are not relevant for 
              #preprocessing and will not get any results for them so adding their complaints description as it is.
          
          final_output['Preprocessed Complaints']=preprocessed_complaints
        
          low_model_prediction =[1 if x==1 and y==1 else 0 for x,y in zip(y_pred_sop,y_pred_fc)] #final prediction is low when both sop and fc models predicts low
          print("changed to final+initial with Sop")
          #low_model_prediction =[1 if x==1 and y==1 else 0 for x,y in zip(low_model_prediction,y_pred_ini)] ## adding the result of model trained on initial classification ,#final prediction is low when both models on finac and inital clasification predicts low

          #creating dataframe for medium and subcat model inference
          embd_with_low_pred=pd.DataFrame(embedding_data)
          embd_with_low_pred['prediction']=low_model_prediction#appending result for low complaints
        
          final_prediction = embd_with_low_pred['prediction'].tolist()
          #subcat_model_result=self.subcategory_prediction(embd_with_low_pred.copy(),model_subcategory)
          
          complete_final_prediction = list(np.zeros(len(data)))#including non english sent
          
          for index , prediction in zip(english_language_index , final_prediction): #adding model predictions in the list
            complete_final_prediction[index]=prediction
            
          for val in non_english_complaints:
            index, prediction = val
            complete_final_prediction[index]=prediction #adding prediction for non english complaints i.e - "Complaint is not in english lang" (output like this)
          
          for index in irrelevant_complaints_index:
            complete_final_prediction[index]="Complaint is not in english language" ##adding prediction for irrelevant complaints as well i.e
            #Complaint is not in english lang
          
          final_output['Predicted_Risk']=self.predicted_result_into_risk_category(complete_final_prediction,low='LOW')
          
          #final_output['Predicted_SubCategory']='' #adding columm for predicted subcategory
          #non_english_complaint_index=final_output[final_output['Predicted_Risk']=="Complaint is not in english language"].index.tolist()
          #final_output.loc[non_english_complaint_index,'Predicted_SubCategory']=['NA' for i in  non_english_complaint_index]#need non english complaints
          #index so that we can NA for those complaints
        
          #final_output.loc[english_language_index,'Predicted_SubCategory']=[pred for pred in subcat_model_result['Predicted_SubCategory'].tolist()]#adding
          #original prediction using relevant index value

          return final_output

        except Exception as e:
          raise e
          #print('Exception is {} from function {}'.format(e, "model_prediction"))
    except Exception as e:
      raise e

# COMMAND ----------

class ModelPrediction():
  def __init__(self,embedding_model,PREDICTION_EMBEDDING_PATH=None,queryToFetchFromDB=None,predictionDataCSVPath=None,final_result_path=None,sop_model_path=None,
               fc_model_path=None,save_prediction_data_csv=None):
    self.utilityFunctions_obj= utilityFunctions()    
    self.embeddingPipeline=embeddingPipeline(embedding_model)
    self.prediction=Prediction(self.utilityFunctions_obj,self.embeddingPipeline,PREDICTION_EMBEDDING_PATH)
    self.dfops_obj=DataframeOperations()
    self.sop_model_path=sop_model_path
    self.fc_model_path=fc_model_path
    self.final_result_path=final_result_path
    self.predictionDataCSVPath=predictionDataCSVPath
    self.queryToFetchFromDB=queryToFetchFromDB
    self.save_prediction_data_csv =save_prediction_data_csv

    
    
  def prediction_from_model(self,readFromDb=True,stage=None,sop_low_model_name=None,fc_low_model_name=None,initial_low_model_name=None,subcategory_model_name=None,mlflow=None):
    """
    This function does testing in real time
    : param - readFromDb (True or False Flag - if True pass the query to run while creating the object or if False pass the path to the csv file, default:True)
    : type - Boolean
    : param - openDate (date from which data to be filtered, default:None)
    : type - string
    : param - closeDate (date till which data to be filtered, default:None)
    : type - string
    : return - data with predicted classification column
    : rtype - pandas dataframe
    """
    
    try:
      if readFromDb:
        data = self.utilityFunctions_obj.data_loading_from_database(self.queryToFetchFromDB)
        print(data.shape,'from readfromdb')
      else:
        data = self.utilityFunctions_obj.read_csv(self.predictionDataCSVPath)
        print('data for prediction',data.shape)
        
      #data = self.dfops_obj.filterting_data_using_awareness_date(data,openDate =openDate, closeDate=closeDate) #not needed anymore 
  
      data = self.dfops_obj.removing_na_value(data,['Complaint_Description'])
      print('data shape from ---',data.shape)
      
      data.reset_index(inplace=True,drop=True)
      if len(data) < 1:
          return pd.DataFrame()
     
      # #new mlflow code
      # #'Staging'
      # low_sop_model_mlflow=mlflow_model_loading(sop_low_model_name,stage=stage,mlflow=mlflow)#loading model using mlflow (right now we are picking up version = 1 by default , for production we can set stage - production
      #
      # #but if we pass the current stage then it will load the model according to the stage note- we have to change the stage before loading
      # #by running mlflowStaging file)
      # low_fc_model_mlflow= mlflow_model_loading(fc_low_model_name,stage=stage,mlflow=mlflow)
      # #### adding below line to load the low risk model trained on "intial" classification
      # low_initial_model_mlflow=mlflow_model_loading(initial_low_model_name,stage=stage,mlflow=mlflow)
      # subcategory_model_mlflow= mlflow_model_loading(subcategory_model_name,stage=stage,mlflow=mlflow)

      low_sop_model = self.prediction.load_saved_model(self.sop_model_path)
      low_fc_model = self.prediction.load_saved_model(self.fc_model_path)
        
      final_data_with_risk=self.prediction.model_prediction(data,low_sop_model,low_fc_model)
      
      final_data_with_risk['Pr_id']=data['Pr_id'].tolist()
      final_data_with_risk['Pr_id']=final_data_with_risk['Pr_id'].astype(str)
      data['Pr_id'] = data['Pr_id'].astype(str)
      final_data_with_risk = final_data_with_risk[['Pr_id', 'Complaints','Predicted_Risk']]
      final_data_with_risk = final_data_with_risk.merge(data[["Pr_id", "Actual_Risk"]])
      final_data_with_risk["Feedback"] = ""
      #data['Predicted_Classification']=final_data_with_risk['Predicted Risk'].tolist()#will change this later
      
      #-------------------appending new predicted complaints with old prediction--------------------------
      #final_data_with_risk = pd.concat([final_data_with_risk,predicted_data],axis=0)
      #---------------------------------------------------------------------------------------------------
      # print(final_data_with_risk.columns,'after prediction')
      # print(final_data_with_risk.head())
      # sparkDF=spark.createDataFrame(final_data_with_risk)
      # #sparkDF.write.mode("overwrite").saveAsTable("gms_us_mart.nlpcc_risk_prediction")
      # #sparkDF.write.mode("overwrite").saveAsTable("gms_us_alyt.nlpcc_risk_prediction")
      # sparkDF.write.mode("overwrite").saveAsTable("gms_us_mart.nlpcc_prediction_model_output") #for dev
      #sparkDF.write.mode("overwrite").saveAsTable("gms_us_alyt.nlpcc_prediction_model_output")  #for production
      print("Save prediction data!!!")
      final_data_with_risk.to_csv(self.save_prediction_data_csv, index=False)
      print("Saved prediction data!!!")
      return final_data_with_risk
    
    except Exception as e:
      print(e)
      raise e