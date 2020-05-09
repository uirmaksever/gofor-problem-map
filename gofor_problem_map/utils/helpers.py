import os
from gofor_problem_map.problem_map import models

def is_in_turkey(point):
    turkey = models.Country.objects.get(name_0="Turkey").geom
    is_inside = turkey.contains(point)
    return is_inside

def find_district(point):
    related_district = models.District.objects.filter(geom__contains=point).first()
    return related_district
