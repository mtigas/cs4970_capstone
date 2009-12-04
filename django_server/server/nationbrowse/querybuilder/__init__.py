# coding=utf-8
ALL_MODELS = [
    'places.nation',
    'places.state',
    'places.county',
    'demographics.placepopulation',
    'demographics.crimedata',
    'demographics.socialcharacteristics',
]
APP_MAP = {
    'nation':'places.nation',
    'state':'places.state',
    'county':'places.county',
    'placepopulation':'demographics.placepopulation',
    'crimedata':'demographics.crimedata',
    'socialcharacteristics':'demographics.socialcharacteristics'
}

PLACES_MODELS = ['nation','state','county']
DATA_MODELS = ['placepopulation','crimedata','socialcharacteristics']
