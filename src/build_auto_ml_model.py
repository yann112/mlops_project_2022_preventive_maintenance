#!/usr/bin/env python3
from pathlib import Path
import sys
import logging
import pickle


###path###
here = Path(__file__).resolve()
path_2 = here.parents[2]
path_1 = here.parents[1]
logs_path = path_2/ 'logs'
logs_path.mkdir(parents=True, exist_ok=True)
input_path = path_2 / 'data' / 'train' 
output_path = path_1 / 'model'
output_path.mkdir(parents=True, exist_ok=True)
classes_path = path_1 / 'src' / 'classes'
sys.path.append(str(classes_path))


###import###
from bearings_preventive_maintenance_model import BuildModel


###logger###
logger = logging.getLogger('build_auto_ml_model')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

FileOutputHandler = logging.FileHandler(logs_path / 'build_auto_ml_model.log')
FileOutputHandler.setFormatter(formatter)
logger.addHandler(FileOutputHandler)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

def main():
    try :
        build_model = BuildModel(logger)
        train_dataframe = input_path / 'df_train.csv'
        label_dataframe = input_path / 'df_train_label.csv'
        model = build_model.build_automl_model(train_dataframe, label_dataframe, training_time=3600)
        with open(output_path / 'model', 'wb') as f:
            pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)
        
    except Exception as e:
        self.logger.error(f'{e}')
    
if __name__ == "__main__":
    main()
