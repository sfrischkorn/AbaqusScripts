import Abaqus
from abaqusConstants import *
import Locations
import SizeDistributions
import SizeDistributions.Circle
import Shapes
import Materials
import Mesh



NUM_INCLUSIONS = 2

#Create the material for the matrix
matrix_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Matrix', youngs_modulus=1000, poissons_ratio=0.2)
matrix_mesh = Mesh.Mesh(elem_shape=TRI)

#Define a material for the inclusions
inclusion_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Inclusion', youngs_modulus=2000, poissons_ratio=0.3)

inclusion_mesh = [Mesh.Mesh(elem_shape=QUAD_DOMINATED)] * NUM_INCLUSIONS

#This is going to use the same material for all inclusions
inclusion_materials = [inclusion_material] * NUM_INCLUSIONS

#Create the distribution and location to use, and generate the inclusions
dist = SizeDistributions.Circle.Random(NUM_INCLUSIONS)
loc = Locations.RandomLocation(NUM_INCLUSIONS)

circles = Locations.Location.GenerateInclusions(NUM_INCLUSIONS, dist, loc, inclusion_materials, recurse_attempts=10)

inclusions = zip(circles, inclusion_mesh)

#Output the details of the generated shapes. It will be located in the directory the script is run from(should eb the abaqus temp directory
export_str = Shapes.Circle.ExportInclusions(circles)
with open("geometry.txt", "w") as text_file:
    text_file.write(export_str)

material_str = Materials.Material.export_materials(matrix_material, inclusion_materials)
with open("materials.txt", "w") as text_file:
    text_file.write(material_str)

#Generate the models in abaqus
Abaqus.GenerateModel(inclusions, matrix_material, matrix_mesh)
