#!/usr/bin/env python3
from pathlib import Path
import sys
import logging
import time
import os

###path###
root_path = Path(__file__).parents[2]
logs_path = root_path / 'logs'
logs_path.mkdir(parents=True, exist_ok=True)
input_path = root_path / Path("data/raw_train")
output_path = root_path / Path("data/train")
output_path.mkdir(parents=True, exist_ok=True)
classes_path = root_path / 'mlops_project_2022_preventive_maintenance' / 'src' / 'classes'
sys.path.append(str(classes_path))


###logger###
logger = logging.getLogger('build_train_df')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

FileOutputHandler = logging.FileHandler(logs_path / 'build_train_df.log')
FileOutputHandler.setFormatter(formatter)
logger.addHandler(FileOutputHandler)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

###import###
from bearings_preventive_maintenance_model import BuildModel

def main() :
    timestr = time.strftime("%Y%m%d-%H%M%S")
    build_model = BuildModel(logger)
    logger.info(f"building new dataframe from folder: {input_path}")
    df_train = build_model.build_train_dataframe(input_path)
    # df_train.to_json(output_path / 'df_train.json', orient="split", index=False)
    logger.info(f"saving dataframe to : {output_path/ f'df_train_{timestr}.csv'}")
    logger.info(f"saving dataframe to : {output_path/ f'df_train_label{timestr}.csv'}")     
    df_train.drop(["cycle_before_break","date"], axis=1).to_csv(output_path/ f'df_train_{timestr}.csv', index=False)
    df_train[["file_id", "cycle_before_break"]].to_csv(output_path/ f'df_train_label_{timestr}.csv', index=False)   
    logger.info(f"building done : good job!!!") 
if __name__ == "__main__":
    main()










