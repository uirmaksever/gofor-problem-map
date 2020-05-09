import os
from django.contrib.gis.utils import LayerMapping
import gofor_problem_map.problem_map.models as models

# Auto-generated `LayerMapping` dictionary for Country model
country_mapping = {
    'gid_0': 'GID_0',
    'name_0': 'NAME_0',
    'geom': 'MULTIPOLYGON',
}

country_filepath = "/Users/umutirmaksever/Documents/python_work_mac/gofor-problem-map/gofor_problem_map/gofor_problem_map/static/turkey_all.gpkg"

def run(verbose=True):
    lm = LayerMapping(models.Country, country_filepath, country_mapping, transform=False, layer="gadm36_TUR_0")
    lm.save(strict=True, verbose=True)
