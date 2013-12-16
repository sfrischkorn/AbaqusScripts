import Abaqus
import Locations
import SizeDistributions
import Shapes
import Materials


#NUM_INCLUSIONS = 1
#INCLUSION_SIZE = 0.25
#LOCATION = [(0.5, 0.5)]

NUM_INCLUSIONS = 50
INCLUSION_SIZE = 0.2
#LOCATION = [(0.25, 0.25), (0.75, 0.75)]

#Create the material for the matrix
matrix_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Matrix', youngs_modulus=1000, poissons_ratio=0.2) 

#Define a material for the inclusions
inclusion_material = Materials.MaterialFactory.createMaterial(Materials.materials.ELASTIC, name='Inclusion', youngs_modulus=2000, poissons_ratio=0.3)
#This is going to use the same material for all inclusions
#inclusion_materials = [inclusion_material, inclusion_material, inclusion_material, inclusion_material]
inclusion_materials = [inclusion_material] * NUM_INCLUSIONS

#Create the distribution and location to use, and generate the inclusions
#dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
dist = SizeDistributions.Random(NUM_INCLUSIONS)#, upper=Shapes.Circle.determine_max_radius(0.01, NUM_INCLUSIONS, 2))
#dist = SizeDistributions.Gaussian(num_inclusions=NUM_INCLUSIONS, centre=0.075, stdev=0.02)
#loc = Locations.FixedLocation(generate_lattice=True, num_locations=NUM_INCLUSIONS)
loc = Locations.RandomLocation(NUM_INCLUSIONS, buffersize=0.01, scale_factor=1)
#loc = Locations.FixedLocation(LOCATION)

#trim the sizes and materials to the number of locations, incase not all locations were usable
#NUM_INCLUSIONS = len(loc.locations)
circles = Locations.Location.GenerateInclusions(NUM_INCLUSIONS, dist, loc, inclusion_materials)

#Generate the models in abaqus
Abaqus.GenerateModel(circles, matrix_material)
