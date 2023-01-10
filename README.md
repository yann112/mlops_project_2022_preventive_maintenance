# Yann Maisonneuve
# Projet data MLOPS 


## septembre 2022


## Ce document présente le projet fil rouge de la formation MLOPS datascientest.

## Objectif

L’objectif de ce projet est de déployer et maintenir un modèle de machine learning de manière fiable et efficace dans un environnement de production.


## Architecture générale

La partie MLOPS ne comprend pas le front-end ni la mise en place de la base de données.

la stack technique utilisée sur ce projet est :



* SCIKIT LEARN pour le machine learning
* FASTAPI/UVICORN pour le back end
* DOCKER pour la conteneurisation
* AIRFLOW
* GITHUB

<img src="https://docs.google.com/drawings/d/e/2PACX-1vRj-5h1rHX8isxGqMO7E-lkkDAcw6aEvzaTmAAYqUbyk560HHfPMG9I_TprmYOmk0IWF43FSqc0tPuK/pub?w=756&amp;h=378">

## le modèle


### La provenance des données

Le jeu de donnée utilisé pour ce projet provient du site Kaggle, “[https://www.kaggle.com/datasets/vinayak123tyagi/bearing-dataset](https://www.kaggle.com/datasets/vinayak123tyagi/bearing-dataset)”,  les données ont été générées par le IMS– [www.imscenter.net](www.imscenter.net).


### Le sujet

Quatre roulements ont été installés sur un arbre, des accéléromètres mesurent  toutes les 10 minutes les vibrations du système jusqu'à rupture des roulements. L’objectif étant d’utiliser ces données pour prédire l'état d’usure  des roulements afin de faire de la maintenance préventive.


### Le pipeline d'entraînement

Les données de chaque enregistrement sont disponibles dans un fichier texte sous la forme d’une liste d'accélérations :

- La première étape consiste à transformer les accélérations en données fréquentielles avec une transformée de fourier

- Ensuite toutes les données sont agrégées dans un dataframe d'entraînement

- Enfin une normalisation est effectuée et un modèle auto-ml est entraîné.

###corrélations
On peut voir sur l'image suivante qu'il y a des corrélations assez bonnes entre une hypothèse de dégradation linéaire et l'analyse vibratoire pour le roulement 3, notamment dans les fréquences autour de 1000 hz.

<img src="https://lh6.googleusercontent.com/MMU33ZPe_7ZjWH8-SEw36e9fjubxiJ68LsAdXzut2hObeNn2nP71I73XHye-QlX_QKE=w2400">

## API BACKEND

<img src="https://docs.google.com/drawings/d/e/2PACX-1vTM5uuNrdG9Jp5TrbSwDl-QstJh5TGHhdar9FrzFpes5uwhC6ihyOTUvessJNXq41alfAj-qbJSBku9/pub?w=960&amp;h=720">