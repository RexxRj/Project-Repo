# Databricks notebook source
#importing all required  packages
import pandas as pd
import numpy as np
import mlflow

# COMMAND ----------

# MAGIC %run  ./training

# COMMAND ----------


dbutils.widgets.text('training_embedding_path','/dbfs/FileStore/nlpcc/complaints_embedding_integrated.csv', 'TRAINING_EMBEDDING_PATH') #old data path till 14 oct 2022
#new path - /dbfs/FileStore/nlpcc
#old path- /dbfs/Users/nitin.sharma@takeda.com/NLPCC

EMBEDDING_PATH = dbutils.widgets.get('training_embedding_path').strip()


#MLFLOW_EXPERIMENT_NAME= "/Users/francesco.de-lorenzi@takeda.com/NLPCC-Working-Version/nlpcc-mlflow"
MLFLOW_EXPERIMENT_NAME = "/Shared/NLPCC_WORKING/mlflow_nlpcc" 

#DEV mlflow path - "/Shared/NLPCC_DEV_WORKING/mlflow_dev"
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

#SUBCAT_REGISTERED_MODEL="SUBCAT_MODEL_WORKING"
SUBCAT_REGISTERED_MODEL="SUBCAT_REGISTERED_MODEL_PROD"

version=1

# COMMAND ----------

trainingObj= trainingPipeline(EMBEDDING_PATH)

# COMMAND ----------

trainingObj.subcat_model_training(version,mlflow,MLFLOW_EXPERIMENT_NAME,SUBCAT_REGISTERED_MODEL)

# COMMAND ----------