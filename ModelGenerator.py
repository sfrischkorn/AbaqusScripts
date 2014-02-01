import Abaqus
import Locations
import SizeDistributions
import SizeDistributions.Circle
import Shapes
import Materials



NUM_INCLUSIONS = 50

#Create the material for the matrix
matrix_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Matrix', youngs_modulus=1000, poissons_ratio=0.2)

#Define a material for the inclusions
inclusion_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Inclusion', youngs_modulus=2000, poissons_ratio=0.3)
#This is going to use the same material for all inclusions
inclusion_materials = [inclusion_material] * NUM_INCLUSIONS

#Create the distribution and location to use, and generate the inclusions
dist = SizeDistributions.Circle.Random(NUM_INCLUSIONS)
loc = Locations.RandomLocation(NUM_INCLUSIONS)

circles = Locations.Location.GenerateInclusions(NUM_INCLUSIONS, dist, loc, inclusion_materials, recurse_attempts=10)

#Output the details of the generated shapes. It will be located in the directory the script is run from(should eb the abaqus temp directory
export_str = Shapes.Shape.ExportInclusions(circles, matrix_material)
with open("geometry.txt", "w") as text_file:
    text_file.write(export_str)

#Generate the models in abaqus
Abaqus.GenerateModel(circles, matrix_material)
