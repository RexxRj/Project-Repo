# Databricks notebook source
!pip install mlflow
!pip install xgboost

# COMMAND ----------



# COMMAND ----------

# DBTITLE 1,Importing Packages.
import mlflow 
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix
from urllib.parse import urlparse
import mlflow.pyfunc
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from mlflow.tracking import MlflowClient
from sklearn import svm
import warnings
warnings.filterwarnings("ignore")

# COMMAND ----------

def mlflow_pipeline(runName,modelParaMeter=None,modelMatrix=None,confusionMatrix=None,model=None,
                    confusionMatrixName="extra",modelName=None,mlflow=None,tagValue=None,TrainingData=None):
  
  """
  runName : string
  modelParaMeter : dict
  modelMatrix : dict
  modelName : string 
  mlflow : mlflow object
  """
  try:
    with mlflow.start_run(run_name=runName):#run name helps us to differentiate between various models we 
      #will try during training 
      if modelParaMeter is not None:
        for key , item in modelParaMeter.items():#saving model parameters
          mlflow.log_param(key,item)

      if modelMatrix is not None:
        for key , item in modelMatrix.items():#saving model metrics 
          mlflow.log_metric(key,item)


      if confusionMatrix is not None:
        mlflow.log_artifcat(confusionMatrix,confusionMatrixName)

      if TrainingData is not None:
        #mlflow.log_artifact(TrainingData,"TrainingData")
        pass

      if tagValue is not None:
        mlflow.set_tag("model_type",tagValue) 

      mlflow.sklearn.log_model(model,modelName)#logging model 
  except Exception as e:
    raise e

  #print('After saving logs into experiment {} and run name is {}'.format(experimentName,runName))
      

# COMMAND ----------



# COMMAND ----------

def get_best_model(experimentName,mlflow,taglist=None):
  """
  this function returns the best sop model and fc model on the basis of precision
  
  experimentName : string
  mlflow : mlflow variable 
  rtype : string
  """
  try:
    experiment_id =  dict(mlflow.get_experiment_by_name(experimentName))['experiment_id']
    #mlflow.get_experiment("8928438")
    exp_df=mlflow.search_runs([experiment_id])#this will return datafram having all the values associated with the given experiment id
    best_model_tag_runid_dict=dict()
    for tag_value in taglist:
        #print('tag value is',tag_value)
        tag_exp_df=exp_df[exp_df['tags.model_type']==tag_value]
        #print(tag_exp_df , tag_exp_df['metrics.Precision'])
        tag_exp_df.sort_values(by ='metrics.Precision',ascending=False,inplace=True)
        tag_exp_df.reset_index(drop=True,inplace=True)
        best_tag_run_id=tag_exp_df.loc[0,'run_id']
        best_tag_model_name= tag_exp_df.loc[0,'tags.mlflow.runName']
        tag_full_run_id = 'runs:/' + best_tag_run_id + '/' + best_tag_model_name
        best_model_tag_runid_dict[tag_value]=[tag_full_run_id,best_tag_model_name]
    
   # print(best_model_tag_runid_dict)
    return best_model_tag_runid_dict
    
  except Exception as e:
    raise e


# COMMAND ----------

def register_model(runName,run_id,mlflow,registerModelName='extra'):
  """
  this function registers model using runid and run name
  runName : string
  run_id : string
  """
  try:
    print('run name is this',runName)
    print('run_id is this ',run_id)
    with mlflow.start_run(run_name=runName) as run:
      result=mlflow.register_model(
      run_id,
      registerModelName)
  
  except Exception as e:
    raise e


# COMMAND ----------

def change_mlflow_state(modelName,modelVersion,modelStage,mlflow=None):
  """
  this function helps us to change the state of the model using version.
  
  modelName : string (registered model name)
  modelVersion : int
  modelStage: string 
  """
  try:
    client = mlflow.tracking.MlflowClient()
    client.transition_model_version_stage(name=modelName,
                                          version=modelVersion,
                                          stage=modelStage)
  except Exception as e:
    raise e


def change_state_of_registered_model(registeredModelName=None,state=None,mlflow=None):
  """
  this function helps us to change the state of registered model in case of changing state or deletion of the model.
  registeredModelName = string
  state = string (state name)
  """
  client = MlflowClient()
  if registeredModelName is not None:
    filter_string = "name='{}'".format(registeredModelName)
    results = client.search_registered_models(filter_string=filter_string)
    if state is None:
      raise Exception("Kindly set the state")
    else:
      for res in results:
          for index, mv in enumerate(res.latest_versions):
            try:
              if mv.current_stage=='None' and index==0 and state=='Staging':
                print("name={}; run_id={}; version={}".format(mv.name, mv.run_id, mv.version))
                change_mlflow_state(registeredModelName,mv.version,state,mlflow=mlflow)
              elif  mv.current_stage=='Staging' and state=='Production':#checking state here
                 change_mlflow_state(registeredModelName,mv.version,state,mlflow=mlflow)
                  
            except Exception as e:
              raise e

# COMMAND ----------

def mlflow_model_loading(modelName,modelVersion=1,stage=None,mlflow=None):
  """
  this function loads model and return the prediction
  
  modelName : string
  modelVersion : int 
  rtype : sklearn trained model
  """
  if stage is not None:
    try:
      #model=mlflow.pyfunc.load_model(model_uri=f"models:/{modelName}/{stage}")
      model=mlflow.sklearn.load_model(model_uri=f"models:/{modelName}/{stage}")
    except Exception as e:
      raise e
  else:
    #model=mlflow.pyfunc.load_model(model_uri=f"models:/{modelName}/{modelVersion}")
    raise Exception("Current state of the model is None please change it to Staging or Production State")      
  return model