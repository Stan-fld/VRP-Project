import unittest

from generation.DataGeneration import DataGeneration


class GenerationTest(unittest.TestCase):

    def test_generate_matrix(self):
        dt = DataGeneration(number_of_summit=10, number_of_vehicle=10, max_neighbor=6)
        self.assertEqual(len(dt.data_vehicles), 10)
        self.assertEqual(len(dt.data_summit), 10)
        self.assertEqual(len(dt.data_matrix), 10)

    def test_all_point_linked(self): #todo !
        self.assertTrue(True)
