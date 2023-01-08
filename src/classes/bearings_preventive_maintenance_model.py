#!/usr/bin/env python3
import numpy as np
from scipy.fft import fft, fftfreq
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
# import autosklearn
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from autosklearn.regression import AutoSklearnRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import make_pipeline
import logging 

class FeaturesExtraction:
    def __init__(self, logger=logging.getLogger(__name__)):
        self.float_sampling_rate = 20000 #Hz
        self.logger = logger
        
    def read_file(self,file_path) :
        try :
               return pd.read_csv(file_path,
                              sep='\t',
                              header=None,
                              names=['Bearing1', 'Bearing2', 'Bearing3', 'Bearing4'])
        except Exception as e:
            self.logger.error(f'{e}')

    def time_signal_to_frequency_signal(self,serie_amplitude):
        """
        Transform a temporal signal from a pandas serie to a frequency signal
        using Fast Fourier Transform
        """
        try :
            serie_amplitude = serie_amplitude.head(20000)
            int_length_data = serie_amplitude.shape[0]
            int_oneside = int_length_data//2
            window = signal.windows.hann(int_length_data)
            list_frequencies = fftfreq(int_length_data, 1 / self.float_sampling_rate)[:int_oneside]
            list_fft_complex_coef = fft(serie_amplitude.to_numpy() * window)
            #2 because oneside sqrt(1.5) for hann window total = *1.633
            list_fft_amplitudes = 2 * np.abs(list_fft_complex_coef)[:int_oneside] / np.sqrt(1.50)

            return (list_fft_amplitudes,list_frequencies)

        except Exception as e:
            self.logger.error(f'{e}')
 
    
    def transform_raw_file_to_frequency_df(self,path_raw_file):
        """
        Transform a raw temporal data file to a pandas dataframe 
        with column named like : bearing"x"_frequency.
        """
        try :
            path_raw_file = Path(path_raw_file)
            raw_df = self.read_file(path_raw_file)
            df_output = pd.DataFrame()
            for col_name in raw_df.columns:
                array_amplitude, array_frequency = self.time_signal_to_frequency_signal(raw_df[col_name])
                list_freq_columns_name = [f"{col_name}_{int(freq)}" for freq in array_frequency]
                dictionary = {list_freq_columns_name[len_index]: array_amplitude[len_index] for len_index in range(len(list_freq_columns_name))}
                df_temp = pd.DataFrame(dictionary, index=[0]).astype('float16')
                df_output = pd.concat([df_output,df_temp], axis=1)
                
            str_file_name = path_raw_file.parts[-1]
            df_output.insert(0, "file_id", str_file_name)
            tuple_split_date = str_file_name.split('.')
            str_datetime = str(datetime(year=int(tuple_split_date[0]),
                                        month=int(tuple_split_date[1]),
                                        day=int(tuple_split_date[2]),
                                        hour=int(tuple_split_date[3]),
                                        minute=int(tuple_split_date[4]),
                                        second=int(tuple_split_date[5])))
            df_output.insert(1, "date", str_datetime)
            return df_output

        except Exception as e:
            self.logger.error(f'{e}')

            
class BuildModel:
    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def build_train_dataframe(self,path_to_files):
        """
        Build a train dataframe from raw txt file 
        """
        try :
            
            path_to_files = Path(path_to_files)
            self.logger.info(f"Looking for training files in {path_to_files.name}")
            list_train_files = list(path_to_files.glob('*'))
            self.logger.info(f"{len(list_train_files)} training files available")
            df_train = pd.DataFrame()
            self.logger.info(f"Extracting features")
            Features_Extraction = FeaturesExtraction()
            for file_raw in list_train_files :
                df_temp = Features_Extraction.transform_raw_file_to_frequency_df(file_raw)
                df_train = df_train.append(df_temp)
            df_train = df_train.sort_values(by="date", ascending=False)
            df_train.insert(2, "cycle_before_break", range(df_train.shape[0]))
                 
            self.logger.info(f"Train dataframe ready")
            return df_train
        
        except Exception as e:
            self.logger.error(f'{e}')


    def build_automl_model(self, train_dataframe, label_dataframe, training_time):
        try :
            self.logger.info(f"training the automl model for {training_time} secondes") 
            X = pd.read_csv(train_dataframe, index_col="file_id")
            y = pd.read_csv(label_dataframe, index_col="file_id")
            X_train, X_test, y_train, y_test = \
                train_test_split(X, y, random_state=1)
            scaler = RobustScaler()
            automl = AutoSklearnRegressor(
                        time_left_for_this_task=training_time,
                    )
            pipeline = make_pipeline(scaler, automl)
            pipeline.fit(X_train, y_train)
            y_hat = pipeline.predict(X_test)
            self.logger.info(f"mean_absolute_error: {mean_absolute_error(y_test, y_hat)}")
            
            return pipeline
        
        except Exception as e:
            self.logger.error(f'{e}')

