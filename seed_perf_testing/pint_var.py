# -*- coding: utf-8 -*-
import pint


def get_pint_var_from_pm_value_object(pm_value):
    units = pint.UnitRegistry()
    if '@uom' in pm_value and '#text' in pm_value:
        # this is the correct expected path for unit-based attributes
        string_value = pm_value['#text']
        try:
            float_value = float(string_value)
        except ValueError:
            return {'success': False,
                    'message': 'Could not cast value to float: \"%s\"' % string_value}
        original_unit_string = pm_value['@uom']
        if original_unit_string == u'kBtu':
            pint_val = float_value * units.kBTU
        elif original_unit_string == u'kBtu/ft²':
            pint_val = float_value * units.kBTU / units.sq_ft
        elif original_unit_string == u'Metric Tons CO2e':
            pint_val = float_value * units.metric_ton
        elif original_unit_string == u'kgCO2e/ft²':
            pint_val = float_value * units.kilogram / units.sq_ft
        else:
            return {'success': False,
                    'message': 'Unsupported units string: \"%s\"' % original_unit_string}
        return {'success': True, 'pint_value': pint_val}
