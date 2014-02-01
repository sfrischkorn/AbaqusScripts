import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

import Materials

class MaterialsTests(unittest.TestCase):
    def test_material_name(self):
        mat = Materials.Material("test_name")
        self.assertEqual("test_name", mat.name)

    def test_create_elastic(self):
        mat = Materials.Elastic("test_name", 1000, 2.0)
        self.assertEqual("test_name", mat.name)
        self.assertEqual(1000, mat.youngs_modulus)
        self.assertEqual(2.0, mat.poissons_ratio)

    def test_factory(self):
        mat = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name="mat", youngs_modulus = 20000, poissons_ratio = 2)
        self.assertEqual("mat", mat.name)
        self.assertEqual(20000, mat.youngs_modulus)
        self.assertEqual(2.0, mat.poissons_ratio)

    def test_abaqus_commands(self):
        mat = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name="mat", youngs_modulus = 20000, poissons_ratio = 2)
        commands = mat.generate_material_commands("model", "section")
        self.assertEqual(3, len(commands))

        self.assertEqual("model.materials['mat'].Elastic(table=((20000, 2), ))", commands[1])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MaterialsTests)
    unittest.TextTestRunner(verbosity=2).run(suite)