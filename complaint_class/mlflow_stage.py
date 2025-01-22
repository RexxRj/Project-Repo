# Databricks notebook source
!pip install mlflow

# COMMAND ----------

import mlflow

# COMMAND ----------

# MAGIC %run ./mlflowUtilities

# COMMAND ----------

# SOP_REGISTERED_MODEL="SOP_REGISTERED_MODEL_WORKING"
# FC_REGISTERED_MODEL="FC_REGISTERED_MODEL_WORKING"

# SOP_REGISTERED_MODEL="LOW_NULL_SOP_REGISTERED_MODEL_WORKING"
# FC_REGISTERED_MODEL="LOW_NULL_FC_REGISTERED_MODEL_WORKING"
# SUBCAT_REGISTERED_MODEL="SUBCAT_MODEL_WORKING"
# INITIAL_REGISTERED_MODEL="LOW_NULL_INITIAL_REGISTERED_MODEL_WORKING"

#For testing purpose 
SOP_REGISTERED_MODEL="LOW_NULL_SOP_REGISTERED_MODEL_PROD"
FC_REGISTERED_MODEL="LOW_NULL_FC_REGISTERED_MODEL_PROD"
INITIAL_REGISTERED_MODEL="LOW_NULL_INITIAL_REGISTERED_MODEL_PROD"
SUBCAT_REGISTERED_MODEL="SUBCAT_REGISTERED_MODEL_PROD"

#MLFLOW_EXPERIMENT_NAME= "/Users/francesco.de-lorenzi@takeda.com/NLPCC-Working-Version/nlpcc-mlflow"
MLFLOW_EXPERIMENT_NAME =  "/Shared/NLPCC_WORKING/mlflow_nlpcc"

mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)



# COMMAND ----------

change_state_of_registered_model(registeredModelName=SOP_REGISTERED_MODEL,state='Staging',mlflow=mlflow)
change_state_of_registered_model(registeredModelName=FC_REGISTERED_MODEL,state='Staging',mlflow=mlflow)
change_state_of_registered_model(registeredModelName=INITIAL_REGISTERED_MODEL,state='Staging',mlflow=mlflow)

# COMMAND ----------

change_state_of_registered_model(registeredModelName=SUBCAT_REGISTERED_MODEL,state='Staging',mlflow=mlflow)

# COMMAND ----------