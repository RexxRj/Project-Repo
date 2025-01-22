from training import trainingPipeline
import pandas as pd
from config import embedding_path
import os

app_dir = os.path.dirname(os.path.realpath(__file__))
model_save_path = os.path.join(app_dir, "saved_model")
print(model_save_path)
training_obj =trainingPipeline(embedding_path,model_save_path)

training_obj.low_risk_model_training()