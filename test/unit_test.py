import pandas as pd

from src.classes.bearings_preventive_maintenance_model import FeaturesExtraction 



def test_type_featuresExtraction():
    fex = FeaturesExtraction()
    assert type(fex.time_signal_to_frequency_signal(pd.Series([0,1,2,3,4,5,6]))) is tuple

