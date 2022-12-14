#!/usr/bin/env python3
from pathlib import Path
import sys
import logging


###path###
here = Path(__file__).resolve()
path_2 = here.parents[2]
path_1 = here.parents[1]
logs_path = path_2 / 'logs'
logs_path.mkdir(parents=True, exist_ok=True)
input_path = path_1 / 'test' / 'raw_train_test'
input_path.mkdir(parents=True, exist_ok=True)
output_path = path_1 / 'test' / 'train_df_test'
output_path.mkdir(parents=True, exist_ok=True)
classes_path = path_1 / 'src' / 'classes'
sys.path.append(str(classes_path))


###import###
from bearings_preventive_maintenance_model import BuildModel


###logger###
logger = logging.getLogger('test_build_train_df')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

FileOutputHandler = logging.FileHandler(logs_path / 'test_build_train_df.log')
FileOutputHandler.setFormatter(formatter)
logger.addHandler(FileOutputHandler)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

def main():
    build_model = BuildModel(logger)
    logger.info(f"building new test dataframe from folder: {input_path}")
    df_train = build_model.build_train_dataframe(input_path)
    # df_train.to_json(output_path / 'df_train.json', orient="split", index=False)
    logger.info(f"saving dataframe to : {output_path/ f'df_train.csv'}")
    df_train.drop(["cycle_before_break","date"], axis=1).to_csv(output_path/ 'df_train.csv', index=False)
    df_train[["file_id", "cycle_before_break"]].to_csv(output_path/ 'df_train_label.csv', index=False)
    logger.info(f"building done : good job!!!")

if __name__ == "__main__":
    main()