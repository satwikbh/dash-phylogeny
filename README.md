# Dash: Malware Phylogenetic Tree Application

This is an interactive demo of the malware (virus) spread of 86 different families. List of all the 86 families, year when the malware was encountered, country-wise distribution can be visualized in this demo.

## Introduction

👉 [Explore the app on Heroku](https://dash-phylogeny.herokuapp.com/).

### [Technique/field associated with the instrument]
This is a modified version of the Dash interactive Python framework developed by [Plotly](https://plot.ly/) which was inspired by the excellent [Nextstrain project](https://nextstrain.org/zika?dmin=2014-06-17).

## Requirements
- The Python version required is >= 3 to control this app;
- The list of all packages is listed in requirements file (see requirements.txt);
- The commands to run that will set up this app and get it ready to run : >python3.6 app.py

## How to use the app
The command needed to run the app:
python3.6 app.py

In the [online app](https://dash-phylogeny.herokuapp.com/), you can select a virus, and the evolution of the virus as a phylogeny tree will display with a map and time series of the virus's global spread.

## Resources

External packages used in the project:
- biopython (https://biopython.org/wiki/Documentation)
- nominatim (https://geopy.readthedocs.io/en/stable/)