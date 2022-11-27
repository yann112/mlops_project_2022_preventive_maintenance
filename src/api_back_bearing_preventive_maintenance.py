from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Header
from pydantic import BaseModel
from typing import Dict
import json
import pandas as pd
from pathlib import Path
import sys

###path###
root_path = Path(__file__).parents[2]
test_path = root_path / 'mlops_project_2022_preventive_maintenance' / 'test'
sys.path.append(str(test_path))

import build_train_df
import build_auto_ml_model
import predict_auto_ml
import test_build_train_df
import test_build_auto_ml_model


#
#
#
#   INIT API
#
#
#

api = FastAPI(
    title="mlops_project_2022_preventive_maintenance",
    description=(
        """
        L’objectif de ce projet est de déployer et maintenir un modèle de machine learning
        de manière fiable et efficace dans un environnement de production.\n
        Le sujet:\n
        Quatre roulements ont été installés sur un arbre,
        des accéléromètres mesurent  toutes les 10 minutes les vibrations du système jusqu'à rupture des roulements.
        L’objectif étant d’utiliser ces données pour prédire l'état d’usure  des roulements
        afin de faire de la maintenance préventive.\n
        https://docs.google.com/document/d/1Bj65W-0Xz9G4MyfD0U8YsUl5K-vRJlbTLnJcosFggGk
        """
        ),
    version="0.0.1",
    openapi_tags=[
    {
        'name': 'User',
        'description': 'fonctions relatives au login d\'un utilisateur lambda'
    },
    {
        'name': 'Admin',
        'description': 'fonctions réservées à un utilisateur avec les droits Admin'
    }
])


@api.get('/health', name='health', tags=['Admin'])
async def get_health():
    """
    Check if the api is up and running
    """
    return {"health" : "UAR"}

@api.post('/test_build_train_df', name='test_build_train_df', tags=['Admin'])
async def test_build_training_df():
    """
    Test to build a new training dataframe 
    """
    test_build_train_df.main()
    return {'test_build_train_df' : 'OK'}

@api.post('/build_train_df', name='build_train_df', tags=['Admin'])
async def build_training_df():
    """
    Build a new training dataframe 
    """
    build_train_df.main()
    return {'build_train_df' : 'OK'}

@api.post('/test_build_automl', name='test_build_automl_model', tags=['Admin'])
async def test_build_automl():
    """
    Test to build a new auto ml model
    """
    test_build_auto_ml_model.main()
    return {'test_build_automl_model' : 'OK'}

@api.post('/build_automl', name='build_automl_model', tags=['Admin'])
async def build_automl():
    """
    Build a new auto ml model
    """
    build_auto_ml_model.main()
    return {'build_automl_model' : 'OK'}

@api.get('/predict_automl', name='predict_automl_model', tags=['User'])
async def build_automl():
    """
    Get a prediction from the automl model 
    """
    predict = predict_auto_ml.main()
    return {'build_automl_model' : predict}