# -*- coding: utf-8 -*-
import unittest

from seed_perf_testing.data_prep import generate_properties, generate_values_for_keys, base_keys
from seed_perf_testing.main import create_from_pm_import
from seed_perf_testing.timer import MeasureDuration


class TestOutputs(unittest.TestCase):

    def test_0100_properties_base_keys_no_limit(self):
        single_data = generate_values_for_keys(base_keys, extra_string_key_count=0)
        data_rows_to_create = 100
        full_data_set = generate_properties(single_data, data_rows_to_create)
        with MeasureDuration():
            csv_rows = create_from_pm_import(full_data_set, limit=False, debug_print=False)
        self.assertEqual(data_rows_to_create + 1, len(csv_rows))

    def test_0500_properties_base_keys_no_limit(self):
        single_data = generate_values_for_keys(base_keys, extra_string_key_count=0)
        data_rows_to_create = 500
        full_data_set = generate_properties(single_data, data_rows_to_create)
        with MeasureDuration():
            csv_rows = create_from_pm_import(full_data_set, limit=False, debug_print=False)
        self.assertEqual(data_rows_to_create + 1, len(csv_rows))

    def test_1000_properties_base_keys_no_limit(self):
        single_data = generate_values_for_keys(base_keys, extra_string_key_count=0)
        data_rows_to_create = 1000
        full_data_set = generate_properties(single_data, data_rows_to_create)
        with MeasureDuration():
            csv_rows = create_from_pm_import(full_data_set, limit=False, debug_print=False)
        self.assertEqual(data_rows_to_create + 1, len(csv_rows))
