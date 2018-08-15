# -*- coding: utf-8 -*-
from main import create_from_pm_import
from timer import MeasureDuration


class KeyTypes(object):
    String = 1
    PintValue = 2


def generate_values_for_keys(keys, extra_string_key_count=0):
    output = {}
    for k, v in keys.iteritems():
        if v == KeyTypes.String:
            output[k] = 'abcdefghijklmnopqrstuvwxyz'
        elif v == KeyTypes.PintValue:
            output[k] = {'@uom': 'kBtu', '#text': '3.1415926535'}
    for i in range(extra_string_key_count):
        output[str(i)] = 'abcdefghijklmnopqrstuvwxyz'
    return output


def generate_properties(instance_data, count):
    output = []
    this_count = 0
    while True:
        this_count += 1
        if this_count > count:
            break
        new_object = {}
        for k, v in instance_data.iteritems():
            new_object[k] = v
        output.append(new_object)
    return output


base_keys = {
    u'address_1': KeyTypes.String,
    u'city': KeyTypes.String,
    u'state_province': KeyTypes.String,
    u'postal_code': KeyTypes.String,
    u'county': KeyTypes.String,
    u'country': KeyTypes.String,
    u'property_name': KeyTypes.String,
    u'property_id': KeyTypes.String,
    u'year_built': KeyTypes.String,
}

single_data = generate_values_for_keys(base_keys, extra_string_key_count=10)
full_data_set = generate_properties(single_data, 100000)

with MeasureDuration() as m:
    data = create_from_pm_import(full_data_set, limit=False)
