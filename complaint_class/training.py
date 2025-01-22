#pip install pycld2==0.41
# #importing all required  packages
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pickle
from utils import utilityFunctions, DataframeOperations
import os


#training functions
class TrainingUtilities:
  
  def __init__(self,utilityFunctions_obj):
    self.utility=utilityFunctions()
    self.dfOps = DataframeOperations()

  
  def train_model(self,X,y,model):
    """
    This function trains the model using X->embedded complaint and y->target classes
    : param - X , y
    : type - list
    : param - model
    : type - model object(e.g Logistic, SVM etc)
    : return - trained model on complaints and target classes 
    : rtype - sklearn model type
    """
    try:
      model.fit(X,y)
      return model
    except Exception as e:
      raise e


  def eval_model_training(self,X_test,y_test,model,modelname=" ",probability=False, threshold=None):
    """
    This function evaluates the model using  X_test->embedded complaints and y_test->target classes and return the precision score 
    note:we only use this for training purpose 
    : param - X_test, y_test, probability (this flag is set for loe and medium models which use threshold in prediction)
    : type - list
    : param - model
    : type - model object(e.g trained model Logistic, SVM etc )
    : param - modelname
    : type - string 
    : return - predicted target classes 
    : rtype - list
    """
    
    if probability:
        try:
            probs = model.predict_proba(X_test)
            print(probs)
            y_pred = [0 if i[1] < threshold else 1 for i in probs]
            print("Classification report training with threshold of :{} and model name {}".format(threshold,modelname))
            print(classification_report(y_test, y_pred))
            precision = precision_score(y_test, y_pred)
            return y_pred, precision
            
        except Exception as e:
            raise e
            
    else:
        try:
          y_pred= model.predict(X_test)
          print("Classification report training for : ", modelname)
          print(classification_report(y_test, y_pred))
          precision = precision_score(y_test, y_pred)
          return y_pred, precision
        except Exception as e:
          raise e
  
  def eval_combined_model_training(self,y_test,flag='Final'):
    """
    This function calculate precision score of the model using y_test which have columns with results of prediction from sop model and fc model
    note:we only use this for training purpose 
    : param - y_test
    : type - list
    : return -  precision score
    : rtype - float
    """
    if flag=='Final':
        try:
            y_test["combined_final_prediciton"] =[1 if x==1 and y==1 else 0 for x,y in zip(y_test["sop_model_prediction"],y_test["fc_model_prediction"])]
            print("Classification report training for final & SOP Model on final classification---------")
            print(classification_report(y_test["Target_new_label"],y_test["combined_final_prediciton"]))
            prec_score= precision_score(y_test["Target_new_label"],y_test["combined_final_prediciton"])
            print("Precision score for Combined Model : ",prec_score)

            print("Classification report training for final & SOP Model on initial classification---------")
            print(classification_report(y_test["Target_initial_label"],y_test["combined_final_prediciton"]))
            prec_score= precision_score(y_test["Target_initial_label"],y_test["combined_final_prediciton"])
            print("Precision score for Combined Model : ",prec_score)
        except Exception as e:
            raise e
    else:#testing results on initial classification model
        try:
            #y_test["combined_final_prediciton"] =[1 if initial_res==1 and sop_res==1 else 0 for initial_res, sop_res in zip(y_test["Initial_model_prediction"],y_test["sop_prob_model_prediction"])]
            ##---- below we are combining the results of models on intial and final classification
            y_test["combined_final_prediciton"] =[1 if x==1 and y==1 else 0 for x,y in zip(y_test["sop_model_prediction"],y_test["fc_model_prediction"])]
            y_test["combined_initial_final_prediciton"] =[1 if initial_res==1 and final_res==1 else 0 for initial_res, final_res in zip(y_test["Initial_model_prediction"],y_test["combined_final_prediciton"])]
            
            print("Classification report training for Initial Model ---------")
            print(classification_report(y_test["Target_initial_label"],y_test["Initial_model_prediction"]))

            print("Classification report training for Combined Model on initial classification ---------")
            print(classification_report(y_test["Target_initial_label"],y_test["combined_initial_final_prediciton"]))
            prec_score= precision_score(y_test["Target_initial_label"],y_test["combined_initial_final_prediciton"])
            print("Precision score for Combined Model : ",prec_score)

            print("Classification report training for Combined Model on final classification ---------")
            print(classification_report(y_test["Target_new_label"],y_test["combined_initial_final_prediciton"]))
            prec_score= precision_score(y_test["Target_new_label"],y_test["combined_initial_final_prediciton"])
            print("Precision score for Combined Model : ",prec_score)

        except Exception as e:
            raise e
    

  def add_prediction_in_data(self,dataframe,y_pred,columnName):
    """
    This function adds predicted column into dataframe y_pred->predicted values that need to be added in the dataframe
    dataframe->dataframe where column will attach
    : param - dataframe
    : type - pandas dataframe
    : param - y
    : type - list
    : param - columnName
    : type - string 
    : return - updated dataframe with predicted column
    : rtype - pandas dataframe
    """
    try:
      dataframe[columnName] = y_pred

      return dataframe
    except Exception as e:
      raise e

  def train_test_split_data(self,X,y,test_size=0.25, random_state=42,stratify=None): #need to change it back to 30
    """
    This function splits data into training and testing set X->embedded complaints , y->target classes 
    : param - X
    : type - list
    : param - y
    : type - list
    : param - stratify
    : type -  "x" or "y" (column to stratify)
    : return - training data and testing data  
    : rtype - list 
    """
    try:
      X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=test_size, random_state=random_state,stratify=stratify)

      return X_train,X_test,y_train,y_test
    except Exception as e:
      raise e
  

  def creating_data_for_training(self,embedding_data_path=None, embedding_data=None):

    """
    This function creates data for training using final classification and sop classification
    : param - embedding_data_path
    : type - pandas dataframe
    : return - training data and testing data using final classification and sop classification
    : rtype - list
    """
    try:
      if embedding_data is not None:
        training_data_sop= embedding_data
      else: 
        training_data_sop=self.utility.read_csv(embedding_data_path)
      
      if (training_data_sop.Original.isna().sum() >0): ##if null values present in text column drop them
        training_data_sop= self.dfOps.removing_na_value(training_data_sop,"Original") 
      if (training_data_sop.Target.isna().sum() >0) or (training_data_sop.Initial_classification.isna().sum() >0): ## if null values present in Target column fill it with "LOW"
        training_data_sop= self.dfOps.replace_na_value(training_data_sop,col_name="Target",value_to_fill='Low')
        print('traing data after filling na with low',training_data_sop['Initial_classification'].value_counts(dropna=False))
        training_data_sop= self.dfOps.replace_na_value(training_data_sop,col_name="Initial_classification",value_to_fill='Low')
        print('traing data after filling na with low',training_data_sop['Initial_classification'].value_counts(dropna=False))
        
      print("shape of the full dataset : ", training_data_sop.shape)
    except Exception as e:
        raise e
    
    try:

      #--------- training data for final classification model (filter out such data for which SOP_Classification is other than Low, Medium and High)
      fc_training_data =training_data_sop[(training_data_sop.SOP_classification!="Low") & 
                                          (training_data_sop.SOP_classification!="Medium") & 
                                          (training_data_sop.SOP_classification!="High")]
      

      #--------- training dataset for sop model (filter out such data for which SOP_Classification is either Low, Medium and High)
      relevant_training_data_sop= training_data_sop[(training_data_sop.SOP_classification=="Low") |
                                                    (training_data_sop.SOP_classification=="Medium") | 
                                                    (training_data_sop.SOP_classification=="High")]
 
   
    except Exception as e:
      raise e

      ####----------  train data for sop model training , test data created here will be common for both the models 
      ##### 1) for sop model training
    try:
      X_sop= relevant_training_data_sop.drop(['Target', 'Original', 'Pr_Id','SOP_classification','Initial_classification','Final_Subcategory'],axis=1)
      y_sop= relevant_training_data_sop[['Target',"SOP_classification",'Initial_classification']] #model will be trained on sop_classification, keeping target also so that   after split we can compare values in target column with the predicted value by model

      ## mapping target columns as 1 for Low and 0 for other
      y_sop['sop_new_label'] = [1 if x =='Low' else 0 for x in y_sop["SOP_classification"]]
      y_sop['Target_new_label'] = [1 if x =='Low' else 0 for x in y_sop["Target"]] #for final low risk 
      y_sop['Target_initial_label']=[1 if x =='Low' else 0 for x in y_sop["Initial_classification"]] #for initial low risk

      X_train_sop,X_test,y_train_sop,y_test=self.train_test_split_data(X_sop,y_sop,test_size=0.25)
      
    except Exception as e:
      raise e
      
    try:
      ##### 2) for final class model training
      X_train_fc= pd.concat([fc_training_data.drop(['Target', 'Original', 'Pr_Id','SOP_classification','Initial_classification','Final_Subcategory'],axis=1),X_train_sop], ignore_index = True)
      X_train_fc.reset_index()
      y_train_fc = fc_training_data[['Target',"SOP_classification",'Initial_classification']]
      ## mapping target columns as 1 for Low and 0 for other
      y_train_fc['sop_new_label'] = [1 if x =='Low' else 0 for x in y_train_fc["SOP_classification"]]
      y_train_fc['Target_new_label'] = [1 if x =='Low' else 0 for x in y_train_fc["Target"]] #for final classification
      y_train_fc['Target_initial_label'] = [1 if x =='Low' else 0 for x in y_train_fc["Initial_classification"]] #for initial classification
      ## append
      y_train_fc= pd.concat([y_train_fc,y_train_sop], ignore_index = True)
      y_train_fc.reset_index()

      #print("train and test size for fc model training: ",X_train_fc.shape,X_test.shape)

      
      return X_train_sop, y_train_sop,X_train_fc,y_train_fc,X_test,y_test

    except Exception as e:
      raise e    
  
    
  def sop_model_training(self,X_train_sop,y_train_sop,X_test,y_test,version=None,mlflow=None,experimentName=None):
    """
    Model training function trains model with help of data based on final classification and sop classification
    : param - X_train_sop ,y_train_sop,X_train_fc,y_train_fc,X_test,y_test
    : type - list
    : return - trained model
    : rtype - sklearn model type
    """
    
    try:
          
      svm_clf = svm.SVC(random_state=42,probability=True)
      svm_model = self.train_model(X_train_sop, y_train_sop["sop_new_label"],svm_clf)
      print("SOP Training : Evaluation of SVM Model : ")
      y_pred_svm, precision_svm =self.eval_model_training(X_test,y_test["sop_new_label"],svm_model,"svm")

      #y_pred_prob_svm , _ = self.eval_model_training(X_test,y_test["sop_new_label"],svm_model,"svm",probability=True,threshold=0.70)

      #model name is same as run name for the sake of simplicity.(this will help us while doing the model registration)
      #mlflow_pipeline("SVM_Sop",svm_model.get_params(),modelMatrix={'Precision':precision_svm},model=svm_model,modelName='SVM_Sop',mlflow=mlflow,tagValue="LOW_NULL_SOP",TrainingData=X_train_sop)
        
    except Exception as e:
       raise e
      
    try:
      ## xgb training on sop      
      xgb_clf=XGBClassifier(random_state=42)
      xgb_model = self.train_model(X_train_sop, y_train_sop["sop_new_label"],xgb_clf)
      print("SOP Training : Evaluation of XGB Model : ")
      y_pred_xgb,precision_xgb =self.eval_model_training(X_test,y_test["sop_new_label"],xgb_model, "XGB")
      
      #mlflow_pipeline("XGB_Sop",xgb_model.get_params(),modelMatrix={'Precision':precision_xgb},model=xgb_model,modelName='XGB_Sop',mlflow=mlflow,tagValue="LOW_NULL_SOP",TrainingData=X_train_sop)
      
    except Exception as e:
      raise e  

    try:
      ## lgr training    
      lgr_clf = LogisticRegression(random_state=0)
      lgr_model = self.train_model(X_train_sop, y_train_sop["sop_new_label"],lgr_clf)
      print("SOP Training : Evaluation of LGR Model : ")
      y_pred_lgr, precision_lgr =self.eval_model_training(X_test,y_test["sop_new_label"],lgr_model, "logistic regression")
      #mlflow_pipeline("Lgr_Sop",lgr_model.get_params(),modelMatrix={'Precision':precision_lgr},model=svm_model,modelName='Lgr_Sop',mlflow=mlflow,tagValue="LOW_NULL_SOP",TrainingData=X_train_sop)
         
    except Exception as e:
       raise e
        
    try:
      y_test = self.add_prediction_in_data(y_test,y_pred_svm,"sop_model_prediction") ### adding pred result of svm ,since it is the best model
      
      #y_test = self.add_prediction_in_data(y_test,y_pred_prob_svm,'sop_prob_model_prediction') ##adding probabilitie
      
      return y_test,svm_model
  
    except Exception as e:
      raise e 
  
  def initial_model_training(self,X_train,y_train,X_test,y_test,version,mlflow,experimentNameInitial):
 
    """
    Model training function trains model with help of data based on initial classification and sop classification
    : param - X_train,y_trai,X_test,y_test (Note:pass y_test generated from sop_model_training)
    : type - list
    : return - trained model
    : rtype - sklearn model type
    """
  
    try:
          
      svm_clf = svm.SVC(random_state=42,probability=True)
      svm_model = self.train_model(X_train, y_train["Target_initial_label"],svm_clf)
      #y_pred_svm, precision_svm =self.eval_model_training(X_test,y_test["Target_initial_label"],svm_model,"svm on initial",probability=True,threshold=0.70)
      y_pred_svm, precision_svm =self.eval_model_training(X_test,y_test["Target_initial_label"],svm_model,"svm on initial")

      #mlflow_pipeline("SVM_Initial",svm_model.get_params(),modelMatrix={'Precision':precision_svm},model=svm_model,modelName='SVM_Initial',mlflow=mlflow,tagValue="LOW_NULL_INI",TrainingData=X_train)
        
    except Exception as e:
       raise e
      
    try:
      ## xgb training on sop      
      xgb_clf=XGBClassifier(random_state=42)
      xgb_model = self.train_model(X_train, y_train["Target_initial_label"],xgb_clf)
      y_pred_xgb,precision_xgb =self.eval_model_training(X_test,y_test["Target_initial_label"],xgb_model, "XGB on initial")
      
      #integrating mlflow code 
      #"XGB_"+version
      #mlflow_pipeline("XGB_Initial",xgb_model.get_params(),modelMatrix={'Precision':precision_xgb},model=xgb_model,modelName='XGB_Initial',mlflow=mlflow,tagValue="LOW_NULL_INI",TrainingData=X_train)
      
      
    except Exception as e:
      raise e  

    try:
      ## lgr training    
      lgr_clf = LogisticRegression(random_state=0)
      lgr_model = self.train_model(X_train, y_train["Target_initial_label"],lgr_clf)
      y_pred_lgr, precision_lgr =self.eval_model_training(X_test,y_test["Target_initial_label"],lgr_model, "logistic regression for Initial")
      
      #mlflow_pipeline("LogisticRegression_Initial",lgr_model.get_params(),modelMatrix={'Precision':precision_lgr},model=lgr_model,modelName='LogisticRegression_Initial',mlflow=mlflow,tagValue="LOW_NULL_INI",TrainingData=X_train)

    except Exception as e:
       raise e
    
    try:
      y_test = self.add_prediction_in_data(y_test,y_pred_svm,"Initial_model_prediction")
      
      return y_test

    except Exception as e:
      raise e
    
  def fc_model_training(self,X_train_fc,y_train_fc,X_test,y_test,version=None,mlflow=None,experimentNameFc=None):
 
    """
    Model training function trains model with help of data based on final classification and sop classification
    : param - X_train_sop ,y_train_sop,X_train_fc,y_train_fc,X_test,y_test (Note:pass y_test generated from sop_model_training)
    : type - list
    : return - trained model
    : rtype - sklearn model type
    """
  
    try:
          
      svm_clf = svm.SVC(random_state=42,probability=True)
      svm_model = self.train_model(X_train_fc, y_train_fc["Target_new_label"],svm_clf)
      y_pred_svm, precision_svm =self.eval_model_training(X_test,y_test["Target_new_label"],svm_model,"svm on fc")
      
      #mlflow_pipeline("SVM",svm_model.get_params(),modelMatrix={'Precision':precision_svm},model=svm_model,modelName='SVM',mlflow=mlflow,tagValue="LOW_NULL_FC",TrainingData=X_train_fc)
        
    except Exception as e:
       raise e
      
    try:
      ## xgb training on sop      
      xgb_clf=XGBClassifier(random_state=42)
      xgb_model = self.train_model(X_train_fc, y_train_fc["Target_new_label"],xgb_clf)
      y_pred_xgb,precision_xgb =self.eval_model_training(X_test,y_test["Target_new_label"],xgb_model, "XGB on fc")
      
      #integrating mlflow code 
      #"XGB_"+version
      #mlflow_pipeline("XGB",xgb_model.get_params(),modelMatrix={'Precision':precision_xgb},model=xgb_model,modelName='XGB',mlflow=mlflow,tagValue="LOW_NULL_FC",TrainingData=X_train_fc)
      
      
    except Exception as e:
      raise e  

    try:
      ## lgr training    
      lgr_clf = LogisticRegression(random_state=0)
      lgr_model = self.train_model(X_train_fc, y_train_fc["Target_new_label"],lgr_clf)
      y_pred_lgr, precision_lgr =self.eval_model_training(X_test,y_test["Target_new_label"],lgr_model, "logistic regression for fc")
      
      #mlflow_pipeline("LogisticRegression",lgr_model.get_params(),modelMatrix={'Precision':precision_lgr},model=lgr_model,modelName='LogisticRegression',mlflow=mlflow,tagValue="LOW_NULL_FC",TrainingData=X_train_fc)

    except Exception as e:
       raise e
    
    try:
      y_test = self.add_prediction_in_data(y_test,y_pred_svm,"fc_model_prediction")
      
      return y_test,svm_model

    except Exception as e:
      raise e
#######------ added for LOE Subcategory -------------########
  def creating_data_for_subcat_loe_training(self,embedding_data_path=None, embedding_data=None):

     """
     This function creates data for training for SubCategory Model
     : param - embedding_data_path
     : type - pandas dataframe
     : return - training data and testing data for SubCategory Model
     : rtype - list
     """
     try:
       if embedding_data is not None:
         training_data= embedding_data
       else: 
         training_data=self.utility.read_csv(embedding_data_path)
            
       if (training_data.Original.isna().sum() >0): ##if null values present in text column drop them
         training_data= self.dfOps.removing_na_value(training_data,"Original")

       if (training_data.Final_Subcategory.isna().sum()>0): ##if null values present in text column drop them
         print('before replacing',training_data['Final_Subcategory'].value_counts(dropna=False))
         training_data= self.dfOps.replace_na_value(training_data,["Final_Subcategory"],value_to_fill="Lack of Effect")
         print('before replacing',training_data['Final_Subcategory'].value_counts(dropna=False))
         

       print("shape of the full dataset : for LOE Model :  ", training_data.shape)
     except Exception as e:
         raise e

     try:
        ## fc_low_training_df=training_data[training_data["Target"]=="Low"] 
         fc_training_df=training_data ####---(instead of training the LOE model only on low risk data, we are training on all data (since the prediction is on low risk model and that   is not 100% precise, so there will be some non low risk data which can be predicted as "LOW". So, to handle that , we use all data to train the LOE model.)
         print("shape of low risk train dataset : for LOE Model : ", fc_training_df.shape)
         ##- labelling the sub categories as 1 for LOE and 0 for other
         fc_training_df["subCat_label"]=[1 if x =='Lack of Effect' else 0 for x in fc_training_df["Final_Subcategory"]]
     except Exception as e:
       raise e

     try:

       X_train_loe = fc_training_df.drop(["Pr_Id","Original","Target","SOP_classification","Final_Subcategory","subCat_label",'Initial_classification'],axis=1)     
       X_train_loe.reset_index()
       y_train_loe = fc_training_df['subCat_label']
       X_train,X_test,y_train,y_test=self.train_test_split_data(X_train_loe,y_train_loe,test_size=0.25)

       return X_train,X_test,y_train,y_test

     except Exception as e:
       raise e    

  def loe_subcat_training(self,X_train,y_train,X_test,y_test,version,mlflow,experimentName):
     """
     Model training function to train model on LOE subcategory
     : param - X_train ,y_train,X_test,y_test,version,mlflow,experimentName
     : type - list
     : return - trained model
     : rtype - sklearn model type
     """
     try:
       svm_clf= svm.SVC(C=1, gamma=1,probability=True)
       svm_clf_low_df = self.train_model(X_train, y_train,svm_clf)
       y_pred_svm, precision_svm =self.eval_model_training(X_test,y_test,svm_clf_low_df,"svm_loe",probability=True, threshold=0.85)
       #mlflow_pipeline("SVM_subcat",svm_clf_low_df.get_params(),modelMatrix={'Precision':precision_svm},model=svm_clf_low_df,modelName='SVM_subcat',mlflow=mlflow,tagValue="Subcat")
       print('precision of loe subcat model',precision_svm)

       return svm_clf

     except Exception as e:
        raise e

  def save_model(self,model,modelname,model_path):
    try:
        model_path = os.path.join(model_path,modelname)
        print(model_path)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
    except Exception as e:
        raise e


class trainingPipeline:
  
  def __init__(self,embedding_saving_path=None,model_save_path=None):
    
    self.utilityFunctions_obj= utilityFunctions() 
    self.dfops_obj=DataframeOperations()
    self.embedding_saving_path= embedding_saving_path
    self.training_obj=TrainingUtilities(self.utilityFunctions_obj)
    self.model_save_path = model_save_path
      
  def low_risk_model_training(self,version=None,mlflow=None,experimentName=None,fc_registered_model_name=None,sop_registered_model_name=None,initial_registered_model_name=None):
     """
     Model training pipeline for low risk
     : param - model version,mlflow,experimentName,fc_registered_model_name,sop_registered_model_name
     : type - list
     : return - None
     """
     try:
       #print('new model training ----------------------------------------------------')
       X_train_sop, y_train_sop,X_train_fc,y_train_fc,X_test,y_test = self.training_obj.creating_data_for_training(embedding_data_path=\
                                                                                                                self.embedding_saving_path)
       print(X_train_sop.shape, y_train_sop.shape,X_train_fc.shape,y_train_fc.shape,X_test.shape,y_test.shape)
       #print('training for sop model for low --------------------------------------')
       y_test,svm_model_sop = self.training_obj.sop_model_training(X_train_sop,y_train_sop,X_test,y_test,version,mlflow,experimentName)
       #print('training for final classification model for low -----------------------------------------------')
       y_test,svm_model_fc = self.training_obj.fc_model_training(X_train_fc,y_train_fc,X_test,y_test,version,mlflow,experimentName)
       #print('training for initial model for low -------------------------------------------------------')
       y_test = self.training_obj.initial_model_training(X_train_fc,y_train_fc,X_test,y_test,version,mlflow,experimentName)
     
       self.training_obj.eval_combined_model_training(y_test)
       #self.training_obj.eval_combined_model_training(y_test,flag='Initial') #checking for initial model with sop
       # best_model_dict=get_best_model(experimentName,mlflow,taglist=['LOW_NULL_FC','LOW_NULL_SOP','LOW_NULL_INI'])#function in mlflowtest
       #
       # register_model(best_model_dict["LOW_NULL_FC"][1],best_model_dict['LOW_NULL_FC'][0],mlflow,fc_registered_model_name)
       # register_model(best_model_dict["LOW_NULL_SOP"][1],best_model_dict['LOW_NULL_SOP'][0],mlflow,sop_registered_model_name)
       # register_model(best_model_dict["LOW_NULL_INI"][1],best_model_dict['LOW_NULL_INI'][0],mlflow,initial_registered_model_name)
       self.training_obj.save_model(svm_model_sop,"sop_model.pkl",self.model_save_path)
       self.training_obj.save_model(svm_model_fc,"fc_model.pkl", self.model_save_path)
       print("LOW Risk Model training completed!")
     
     except Exception as e:
       raise e

        
        
  def subcat_model_training(self,version,mlflow,experimentName,subcat_registered_model_name):
    """
     Model training pipeline for subcategory.
     : param -  model version,mlflow,experimentName,subcat_registered_model_name
     : type - list
     : return - None
     """
    
    try:
      print('from subcat training')
    
      X_train_loe,X_test_loe,y_train_loe,y_test_loe=self.training_obj.creating_data_for_subcat_loe_training(embedding_data_path=self.embedding_saving_path)        
        
      print(X_train_loe.shape, y_train_loe.shape,X_test_loe.shape,y_test_loe.shape)
    
      subcat_model = self.training_obj.loe_subcat_training(X_train_loe,y_train_loe,X_test_loe,y_test_loe,version,mlflow,experimentName)
     
      # best_model_dict=get_best_model(experimentName,mlflow,taglist=['Subcat'])#function in mlflowtest
      #
      # register_model(best_model_dict["Subcat"][1],best_model_dict['Subcat'][0],mlflow,subcat_registered_model_name)
        
      print("Subcat Model training completed!")
    except Exception as e:
        raise e


# COMMAND ----------