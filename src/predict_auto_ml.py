#!/usr/bin/env python3
from pathlib import Path
import sys
import logging
import pickle
import pandas as pd

###path###
here = Path(__file__).resolve()
path_2 = here.parents[2]
path_1 = here.parents[1]
logs_path = path_2 / 'logs'
logs_path.mkdir(parents=True, exist_ok=True)
input_path = path_2 / 'data' / 'raw_test'
input_path.mkdir(parents=True, exist_ok=True)
output_path = path_2 / 'data' / 'predict'
output_path.mkdir(parents=True, exist_ok=True)
model_path = path_1 / 'model'
model_path.mkdir(parents=True, exist_ok=True)
classes_path = path_1 / 'src' / 'classes'
sys.path.append(str(classes_path))


###import###
from bearings_preventive_maintenance_model import FeaturesExtraction



###logger###
logger = logging.getLogger('predict_auto_ml_model')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

FileOutputHandler = logging.FileHandler(logs_path / 'predict_auto_ml_model.log')
FileOutputHandler.setFormatter(formatter)
logger.addHandler(FileOutputHandler)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

def main():
    try :
        df_output = pd.DataFrame()
        with open(model_path / 'model', 'rb') as f:
            model = pickle.load(f)
        features_extraction = FeaturesExtraction(logger)
        for file in input_path.glob('*') :
            df_predict = features_extraction.transform_raw_file_to_frequency_df(file)
            X = df_predict.drop(["file_id", "date"], axis=1)
            prediction = round(model.predict(X)[0],2)
            df_temp = pd.DataFrame(
                {'filename' : df_predict['file_id'].unique(),
                'date' : df_predict['date'].unique(),
                'prediction' : prediction}
                ) 
            df_output = pd.concat([df_output, df_temp], ignore_index=True)
            
        return df_output
        
    except Exception as e:
        logger.error(f'{e}')
    
if __name__ == "__main__":
    main()
