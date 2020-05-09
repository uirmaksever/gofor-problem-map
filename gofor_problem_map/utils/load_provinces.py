import os
from django.contrib.gis.utils import LayerMapping
import gofor_problem_map.problem_map.models as models

# Auto-generated `LayerMapping` dictionary for Province model
province_mapping = {
    'gid_0': 'GID_0',
    'name_0': 'NAME_0',
    'gid_1': 'GID_1',
    'name_1': 'NAME_1',
    'varname_1': 'VARNAME_1',
    'nl_name_1': 'NL_NAME_1',
    'type_1': 'TYPE_1',
    'engtype_1': 'ENGTYPE_1',
    'cc_1': 'CC_1',
    'hasc_1': 'HASC_1',
    'geom': 'MULTIPOLYGON',
}

provinces_filepath = "/Users/umutirmaksever/Documents/python_work_mac/gofor-problem-map/gofor_problem_map/gofor_problem_map/static/turkey_all.gpkg"

def run(verbose=True):
    lm = LayerMapping(models.Province, provinces_filepath, province_mapping, transform=False, layer="gadm36_TUR_1")
    lm.save(strict=True, verbose=True)
