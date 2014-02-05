import unittest
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from mock import Mock
sys.modules['abaqusConstants'] = Mock()
import abaqusConstants

import Mesh

class MeshTests(unittest.TestCase):
    def test_wrong_elem_shape(self):
        self.assertRaises(AssertionError, Mesh.Mesh, elem_shape='blerg')

    def test_elem_shape(self):
        mesh = Mesh.Mesh(elem_shape=abaqusConstants.TET)
        self.assertEqual(abaqusConstants.TET, mesh.elem_shape)

    def test_algorithm_correct(self):
        mesh = Mesh.Mesh(elem_shape=abaqusConstants.QUAD, technique=abaqusConstants.FREE, algorithm=abaqusConstants.MEDIAL_AXIS)
        self.assertEqual(abaqusConstants.QUAD, mesh.elem_shape)
        self.assertEqual(abaqusConstants.FREE, mesh.technique)
        self.assertEqual(abaqusConstants.MEDIAL_AXIS, mesh.algorithm)

    def test_algorithm_wrong(self):
        self.assertRaises(AssertionError, Mesh.Mesh, elem_shape=abaqusConstants.HEX, technique=abaqusConstants.FREE, algorithm=abaqusConstants.MEDIAL_AXIS)

    #def test_generatecommands(self):
    #    mesh = Mesh.Mesh(elem_shape=abaqusConstants.QUAD, technique=abaqusConstants.FREE, algorithm=abaqusConstants.MEDIAL_AXIS)
    #    command = mesh.GenerateCommand("matrixRegion")

    #    self.assertEqual("p.setMeshControls(regions=matrixRegion, elemShape=QUAD, technique=FREE, algorithm=MEDIAL_AXIS)", command)

    def test_generatecommands_none(self):
        mesh = Mesh.Mesh()
        command = mesh.GenerateCommand("matrixRegion")

        self.assertEqual("p.setMeshControls(regions=matrixRegion)", command)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MeshTests)
    unittest.TextTestRunner(verbosity=2).run(suite)