# -*- coding: utf-8 -*-
import unittest

from seed_perf_testing.data_prep import generate_properties, generate_values_for_keys, base_keys
from seed_perf_testing.main import create_from_pm_import
from seed_perf_testing.timer import MeasureDuration


class TestOutputs(unittest.TestCase):

    def test_a(self):
        single_data = generate_values_for_keys(base_keys, extra_string_key_count=10)
        full_data_set = generate_properties(single_data, 100)
        with MeasureDuration() as m:
            data = create_from_pm_import(full_data_set, limit=False)
        self.assertEqual(100, len(data))
