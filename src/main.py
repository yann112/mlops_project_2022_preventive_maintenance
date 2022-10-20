import mlops_project_2022_preventive_maintenance

if __name__ == "__main__":
    file_path = '/kaggle/input/bearing-dataset/3rd_test/4th_test/txt/'
    build_model = BuildModel()
    df_train = build_model.build_train_dataframe(file_path)