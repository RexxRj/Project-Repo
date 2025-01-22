# Databricks notebook source
#importing all required  packages
import pandas as pd
import numpy as np
import mlflow

# COMMAND ----------

# MAGIC %run  ./training

# COMMAND ----------

dbutils.widgets.text('training_embedding_path','/dbfs/FileStore/nlpcc/complaints_embedding_integrated.csv', 'TRAINING_EMBEDDING_PATH') #old training data path till 14th oct 2022

EMBEDDING_PATH = dbutils.widgets.get('training_embedding_path').strip()


MLFLOW_EXPERIMENT_NAME = "/Shared/NLPCC_WORKING/mlflow_nlpcc"
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

SOP_REGISTERED_MODEL="LOW_NULL_SOP_REGISTERED_MODEL_PROD"
FC_REGISTERED_MODEL="LOW_NULL_FC_REGISTERED_MODEL_PROD"
INITIAL_REGISTERED_MODEL="LOW_NULL_INITIAL_REGISTERED_MODEL_PROD"

version=1

# COMMAND ----------

trainingObj= trainingPipeline(EMBEDDING_PATH)

# COMMAND ----------

trainingObj.low_risk_model_training(version,mlflow,MLFLOW_EXPERIMENT_NAME,FC_REGISTERED_MODEL,SOP_REGISTERED_MODEL,INITIAL_REGISTERED_MODEL)

# COMMAND ----------