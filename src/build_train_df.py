#!/usr/bin/env python3
from pathlib import Path
from classes.bearings_preventive_maintenance_model import BuildModel

root_path = Path(__file__).parents[2]
input_path = root_path / Path("data/raw_train")
output_path = root_path / Path("data/raw_train")

if __name__ == "__main__":
    build_model = BuildModel()
    df_train = build_model.build_train_dataframe(input_path)
    df_train.to_csv(output_path, index=False)