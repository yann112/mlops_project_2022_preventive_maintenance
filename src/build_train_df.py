#!/usr/bin/env python3
from pathlib import Path
import sys
import logging

###path###
root_path = Path(__file__).parents[2]
logs_path = root_path / 'logs'
logs_path.mkdir(parents=True, exist_ok=True)
input_path = root_path / Path("data/raw_train")
output_path = root_path / Path("data/train")
output_path.mkdir(parents=True, exist_ok=True)
classes_path = root_path / 'mlops_project_2022_preventive_maintenance' / 'src' / 'classes'
sys.path.append(str(classes_path))
root_path = Path(__file__).parents[2]

###logger###
logger = logging.getLogger('test_train_df')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

###import###
from bearings_preventive_maintenance_model import BuildModel

    
if __name__ == "__main__":
    build_model = BuildModel(logger)
    df_train = build_model.build_train_dataframe(input_path)
    # df_train.to_json(output_path / 'df_train.json', orient="split", index=False)    
    df_train.drop(["cycle_before_break","date"], axis=1).to_csv(output_path/ 'df_train.csv', index=False)
    df_train[["file_id", "cycle_before_break"]].to_csv(output_path/ 'df_train_label.csv', index=False)










