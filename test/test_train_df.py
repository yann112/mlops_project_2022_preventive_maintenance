#!/usr/bin/env python3
from pathlib import Path
import sys
import logging

root_path = Path(__file__).parents[2]
logs_path = root_path / 'logs'
logs_path.mkdir(parents=True, exist_ok=True)
input_path = root_path / 'mlops_project_2022_preventive_maintenance' / 'test' / 'raw_train_test'
input_path.mkdir(parents=True, exist_ok=True)
output_path = root_path / 'mlops_project_2022_preventive_maintenance' / 'test' / 'output_test'
output_path.mkdir(parents=True, exist_ok=True)
classes_path = root_path / 'mlops_project_2022_preventive_maintenance' / 'src' / 'classes'
sys.path.append(str(classes_path))
from bearings_preventive_maintenance_model import BuildModel

###logger###
logger = logging.getLogger('test_train_df')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


if __name__ == "__main__":
    build_model = BuildModel(logger)
    df_train = build_model.build_train_dataframe(input_path)
    df_train.to_csv(output_path / 'df_train.csv', index=False)