import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report, accuracy_score
import regex as re
import nltk
from nltk.tokenize import word_tokenize
from langdetect import detect
import numpy as np
import joblib
import os

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

class PreprocessData():
    
    def __init__(self,dataframe):
        self.dataframe = dataframe
        
    
    def replace_na_value(self,dataframe,col_name="Category", value_to_fill="NA"):
        """
        This function replaces na values for the given column with the value provided to replace it with. 
        Specially created to fill na values in Final Classification column with "NA".
        
        : param - dataframe
        : type - pandas dataframe
        : param - col_name (default= "Final_Classification")
        : type - list 
        : param - value_to_fill (default ="NA")
        : type - string  
        : return - dataframe after replacing nan value 
        : rtype - pandas dataframe
        """
        try:
        
            dataframe[col_name]=dataframe[col_name].fillna(value_to_fill)
            
            return  dataframe
        except Exception as e:
            raise e
    
    def removing_na_value(self,dataframe,col_names):#remove na value for given columns
        """
        This function removes na values for the given columns
        : param - dataframe
        : type - pandas dataframe
        : param - col_names
        : type - list 
        : return - dataframe after remoing nan value 
        : rtype - pandas dataframe
        """
        try:
        #dataframe=dataframe.fillna(value=np.nan)
            original_dataframe = dataframe.copy()
            dataframe=dataframe.dropna(subset=col_names)
            dropped_rows = original_dataframe[~original_dataframe.index.isin(dataframe.index)]
            print(len(dropped_rows))
            
            return dataframe
        except Exception as e:
            raise e
    
    
    
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
        re_bad_chars= re.compile(r"[\p{Cc}\p{Cs}]+")
        
        try:
            return re_bad_chars.sub("", text)
        
        except Exception as e:
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
                if len(tmp_list)>0: 
                    relevant_complaints_list.append(" ".join(tmp_list))
                else:
                    print(tmp_list)
                    if flag:
                        index_irrelevant_complaints.append(english_language_index[index])
                    else:
                        index_irrelevant_complaints.append(index)
                
            return relevant_complaints_list,index_irrelevant_complaints
        
        except Exception as e:
            print('Error Occurred: ',e)
            raise e
        
    
    def preprocessing_training_data(self):
        """
        This function performs preprocessing on the training data by removing different languages and sentence preprocessing.
        : param - dataframe
        : type - pandas dataframe 
        : return - return training data with processed complaints text and sop classification  
        : rtype - pandas dataframe
        """
        
        try:
            df = self.dataframe
            
            cols = df.columns
            
            for col in cols:
                print("Dropna for Col: ",col)
                df = self.removing_na_value(df,col)
        except Exception as e:
            raise e
        
        try:
            list_of_sents=df['Merchant'].tolist()
            
            list_of_sents , list_of_indices_to_rem=self.sent_preprocessing(list_of_sents)#sentence preprocessing
            
            print(list_of_indices_to_rem)
        except Exception as e:
            raise e
        
        try:
            df=df.drop(df.index[list_of_indices_to_rem],axis=0)
            df.reset_index(inplace=True)
            
            target = df['Category'].tolist()
            
            training_data = pd.DataFrame({'Data':list_of_sents,'Target': target})
            
        except Exception as e:
            raise e
        
        try:
            df=df.fillna(value=np.nan)
            training_data['Category']=df['Category']
            return training_data
        
        except Exception as e:
            raise e
    
    
class TrainModel():
        
    def __init__(self,training_data):
        self.training_data = training_data
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
    def save_model(self,model,vectorizer,label_encoder):
        joblib.dump(vectorizer, 'vectorizer.pkl')
        joblib.dump(model, 'model.pkl')
        joblib.dump(label_encoder, 'label_encoder.pkl')
        print("Model saved")
        
    
    def train_model(self):
        
        merchants = self.training_data.values('merchant')
        merchants = [merchant['merchant'] for merchant in merchants]
        categories = self.training_data.values('category')
        categories = [category['category'] for category in categories]
        
        data = pd.DataFrame({'Merchant':merchants,'Category':categories})
        
        preprocessor = PreprocessData(data)

        data = preprocessor.preprocessing_training_data()
        
        
        
        X = data['Target']
        y = data['Category']
        
        label_encoder = LabelEncoder()
        
        
        vectorizer_path = os.path.join(self.current_dir, "saved_models", "vectorizer.pkl")
        model_path = os.path.join(self.current_dir, "saved_models", "model.pkl")
        label_encoder_path = os.path.join(self.current_dir, "saved_models", "label_encoder.pkl")

        loaded_vectorizer = joblib.load(vectorizer_path)
        loaded_model = joblib.load(model_path)
        loaded_label_encoder = joblib.load(label_encoder_path)
        
        #update vectorizer
        new_vectorizer = CountVectorizer()
        new_vectorizer.fit(X) 

        combined_vocab = loaded_vectorizer.vocabulary_

        for word, idx in new_vectorizer.vocabulary_.items():
            if word not in combined_vocab:
                combined_vocab[word] = len(combined_vocab)

        loaded_vectorizer.vocabulary_ = combined_vocab
        
        #update label encoder
        new_categories = y.unique()
        all_categories = list(loaded_label_encoder.classes_) + list(new_categories)
        all_categories = sorted(set(all_categories))
        label_encoder.fit(all_categories)
        
        
        # vectorizer = CountVectorizer()
        X_transformed = loaded_vectorizer.fit_transform(X)
        y_transformed = label_encoder.transform(y)

        X_train, X_test, y_train, y_test = train_test_split(X_transformed, y_transformed, test_size=0.2, random_state=42)

        # Retrain the model
        loaded_model.fit(X_train, y_train)

        # Evaluate
        print("Model retrained with feedback:")
        print(loaded_model.score(X_test, y_test))
        
        self.save_model(loaded_model, loaded_vectorizer, label_encoder)

class PredictModel():
    
    def __init__(self, merchant):
        self.merchant = merchant
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
    
    def predict(self):
        
        label_encoder = LabelEncoder()
        
        
        vectorizer_path = os.path.join(self.current_dir, "saved_models", "vectorizer.pkl")
        model_path = os.path.join(self.current_dir, "saved_models", "model.pkl")
        label_encoder_path = os.path.join(self.current_dir, "saved_models", "label_encoder.pkl")
        
        loaded_vectorizer = joblib.load(vectorizer_path)
        loaded_model = joblib.load(model_path)
        loaded_label_encoder = joblib.load(label_encoder_path)
        
        self.merchant = [self.merchant]
        
        new_merchants_tfidf = loaded_vectorizer.transform(self.merchant)
        predictions = loaded_model.predict(new_merchants_tfidf)
        predicted_categories = loaded_label_encoder.inverse_transform(predictions)
        
        return predicted_categories[0]
            
        