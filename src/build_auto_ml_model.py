#!/usr/bin/env python3
from pathlib import Path
import sys
import logging
import pickle


###path###
root_path = Path(__file__).parents[2]
logs_path = root_path / 'logs'
logs_path.mkdir(parents=True, exist_ok=True)
input_path = root_path / 'data' / 'train' 
output_path = root_path / 'mlops_project_2022_preventive_maintenance' / 'model'
output_path.mkdir(parents=True, exist_ok=True)
classes_path = root_path / 'mlops_project_2022_preventive_maintenance' / 'src' / 'classes'
sys.path.append(str(classes_path))


###import###
from bearings_preventive_maintenance_model import BuildModel


###logger###
logger = logging.getLogger('train_df')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


if __name__ == "__main__":
    try :
        build_model = BuildModel(logger)
        train_dataframe = input_path / 'df_train.csv'
        label_dataframe = input_path / 'df_train_label.csv'
        model = build_model.build_automl_model(train_dataframe, label_dataframe, training_time=3600)
        with open(output_path / 'model', 'wb') as f:
            pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)
            
    except Exception as e:
        self.logger.error(f'{e}')