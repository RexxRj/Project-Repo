import regex
import warnings
warnings.filterwarnings("ignore")
import prediction
import os
from utils import calculate_final_metrics

print("prediction")
app_dir = os.path.dirname(os.path.realpath(__file__))
PREDICTION_EMBEDDING_PATH = os.path.join(app_dir, "data", "prediction_data","pred_embed.csv")
predictionDataCSVPath = os.path.join(app_dir, "data", "prediction_data","prediction_data.csv")
#predictionDataCSVPath = os.path.join(app_dir, "data", "prediction_data","prediction_2.csv")
metricPath = os.path.join(app_dir, "data", "prediction_data","metrics.csv")
save_prediction_data_csv= os.path.join(app_dir, "data", "prediction_data","Final_Prediction.csv")
sop_model_path = os.path.join(app_dir, "saved_model", "sop_model.pkl")
fc_model_path = os.path.join(app_dir, "saved_model", "fc_model.pkl")

EMBEDDING_MODEL="all-MiniLM-L12-v2"
RE_BAD_CHARS = regex.compile(r"[\p{Cc}\p{Cs}]+")

model_predObj = prediction.ModelPrediction(EMBEDDING_MODEL,PREDICTION_EMBEDDING_PATH=PREDICTION_EMBEDDING_PATH,
                                predictionDataCSVPath = predictionDataCSVPath,sop_model_path=sop_model_path,
                                fc_model_path=fc_model_path,save_prediction_data_csv=save_prediction_data_csv)

pred_result = model_predObj.prediction_from_model(readFromDb=False)
metric_df = calculate_final_metrics(pred_result)
metric_df.to_csv(metricPath, index=False)
print(metric_df)

## steps to increase precison/ other metrics
# more data
# high probability threshold
# hyperparameter tuning
# feedback incorportaion