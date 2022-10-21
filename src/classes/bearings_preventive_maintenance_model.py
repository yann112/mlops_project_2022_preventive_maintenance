#!/usr/bin/env python3
import numpy as np
from scipy.fft import fft
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
from pathlib import Path



class FeaturesExtraction:
    def __init__(self, logger):
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
            int_length_data = serie_amplitude.shape[0]
            list_of_frequencies =  list((1/(self.float_sampling_rate * int_length_data)) * np.arange(int_length_data))
            list_fft_complex_coef = fft(serie_amplitude.to_numpy())
            list_fft_amplitudes = np.abs(list_fft_complex_coef)
            #the power spectrum is symetrical get only the positive part
            int_oneside = int_length_data//2
            list_frequencies_oneside = list_of_frequencies[:int_oneside]
            list_amplitude_oneside = list_fft_amplitudes[:int_oneside]
            serie_amplitude
            return (list_amplitude_oneside,list_frequencies_oneside)

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
                list_freq_columns_name = [f"{col_name}_{format(freq, '.2e')}" for freq in array_frequency]
                dictionary = {list_freq_columns_name[len_index]: array_amplitude[len_index] for len_index in range(len(list_freq_columns_name))}
                df_temp = pd.DataFrame(dictionary, index=[0])
                df_output = pd.concat([df_output,df_temp], axis=1)

            df_output.insert(0, "file_id", path_raw_file.parts[-1])
            return df_output

        except Exception as e:
            self.logger.error(f'{e}')

            
class BuildModel:
    def __init__(self, logger):
        self.logger = logger

    def build_train_dataframe(self,path_to_files):
        """
        Build a train dataframe from raw txt file 
        """
        try :
            self.logger.info(f"Looking for training files")
            path_to_files = Path(path_to_files)
            list_train_files = list(path_to_files.glob('*'))
            self.logger.info(f"{len(list_train_files)} training files available")
            df_train = pd.DataFrame()
            self.logger.info(f"Extracting features")
            Features_Extraction = FeaturesExtraction(self.logger)
            for file_raw in list_train_files :
                df_temp = Features_Extraction.transform_raw_file_to_frequency_df(file_raw)
                df_train = df_train.append(df_temp)
            self.logger.info(f"Train dataframe ready")
            return df_train
        
        except Exception as e:
            self.logger.error(f'{e}')

    def build_target_dataframe(self):
        """
        """
        pass

    def model_pipeline(self):
        pass