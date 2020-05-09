import os
from django.contrib.gis.utils import LayerMapping
import gofor_problem_map.problem_map.models as models

# Auto-generated `LayerMapping` dictionary for District model
district_mapping = {
    'gid_0': 'GID_0',
    'name_0': 'NAME_0',
    'gid_1': 'GID_1',
    'name_1': 'NAME_1',
    'nl_name_1': 'NL_NAME_1',
    'gid_2': 'GID_2',
    'name_2': 'NAME_2',
    'varname_2': 'VARNAME_2',
    'nl_name_2': 'NL_NAME_2',
    'type_2': 'TYPE_2',
    'engtype_2': 'ENGTYPE_2',
    'cc_2': 'CC_2',
    'hasc_2': 'HASC_2',
    'geom': 'MULTIPOLYGON',
}

district_filepath = "/Users/umutirmaksever/Documents/python_work_mac/gofor-problem-map/gofor_problem_map/gofor_problem_map/static/ilceler.json"

def run(verbose=True):
    lm = LayerMapping(models.District, district_filepath, district_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
