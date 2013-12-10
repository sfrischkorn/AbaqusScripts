import Locations
import SizeDistributions
import Shapes



from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

def GenerateCircles(num_inclusions, distribution, locations, max_attempts=10000):
    if type(locations) == Locations.FixedLocation:
        if num_inclusions <> len(locations.locations) <> len(distribution.distribution):
                raise IndexError("The number of inclusions and length of the locations must be equal")    
    
    circles = []

    # loop through num inclusions
    for i in range(num_inclusions):
        inclusion = locations.GenerateInclusion(distribution, circles)
        if inclusion:
            circles.append(inclusion)

    return circles

def GenerateModel():
    #Define constants
    modelName = 'Single Inclusion'
    partName = 'Part-1'
    materialName = 'Matrix'
    mySectionName = 'Matrix'
    setName = 'Matrix'

    inclusionMaterialName = 'Inclusion'
    inclusionSectionName = 'Inclusion'
    inclusionSetName = 'Inclusion'

    assemblyName = 'Single Inclusion'

    #create the model
    myModel = mdb.Model(modelName)

    #create a unit square shape
    myModel.ConstrainedSketch(name='__profile__', sheetSize=20.0)
    myModel.sketches['__profile__'].rectangle(point1=(0, 0),point2=(1.0, 1.0))
    myModel.Part(dimensionality=TWO_D_PLANAR, name=partName, type=DEFORMABLE_BODY)
    myModel.parts[partName].BaseShell(sketch=mdb.models[modelName].sketches['__profile__'])
    del myModel.sketches['__profile__']

    p = myModel.parts[partName]
    f = p.faces

    #NUM_INCLUSIONS = 1
    #INCLUSION_SIZE = 0.25
    #LOCATION = [(0.5, 0.5)] 

    NUM_INCLUSIONS = 2
    INCLUSION_SIZE = 0.2
    LOCATION = [(0.25, 0.25), (0.35, 0.35)] 

    dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
    loc = Locations.FixedLocation(LOCATION)

    circles = GenerateCircles(NUM_INCLUSIONS, dist, loc)


    for circle in circles:
        commands = circle.GenerateSketch()

        for command in commands:
            exec(command)
        
        inclusionFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
        p.PartitionFaceBySketch(faces=inclusionFaces, sketch=s)

        del s

    #assign materials
    myModel.Material(name=materialName)
    myModel.materials[materialName].Elastic(table=((1000000000.0, 0.3), ))
    myModel.HomogeneousSolidSection(material=materialName, name=mySectionName, thickness=None)

    myModel.Material(name=inclusionMaterialName)
    myModel.materials[inclusionMaterialName].Elastic(table=((2000000000.0, 0.4), ))
    myModel.HomogeneousSolidSection(material=inclusionMaterialName, name=inclusionSectionName, thickness=None)

    #Create sets and sections
    #session.viewports['Viewport: 1'].setValues(displayedObject=p1)

    inclusionFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    inclusionRegion = p.Set(faces=inclusionFaces, name=inclusionSetName)
    p.SectionAssignment(region=inclusionRegion, sectionName=inclusionSectionName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

    matrixFaces = f.getSequenceFromMask(mask=('[#2 ]', ), )
    matrixRegion = p.Set(faces=matrixFaces, name=setName)
    p.SectionAssignment(region=matrixRegion, sectionName=mySectionName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)


    #Create the assembly
    assembly = myModel.rootAssembly
    assembly.DatumCsysByDefault(CARTESIAN)
    assembly.Instance(name=assemblyName, part=p, dependent=ON)

    regionsToMesh = matrixRegion, inclusionRegion,
    #create the mesh
    p.setMeshControls(regions=inclusionFaces, elemShape=TRI)
    p.seedPart(size=0.1)
    p.generateMesh()








GenerateModel()















#NUM_INCLUSIONS = 1
#INCLUSION_SIZE = 0.25
#LOCATION = [(0.5, 0.5)] 

#dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
#loc = Locations.FixedLocation(LOCATION)

#GenerateCircles(NUM_INCLUSIONS, dist, loc)



#NUM_INCLUSIONS = 2
#INCLUSION_SIZE = 0.2
#LOCATION = [(0.25, 0.25), (0.35, 0.35)] 

#dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
#loc = Locations.FixedLocation(LOCATION)

#circles = GenerateCircles(NUM_INCLUSIONS, dist, loc)



#NUM_INCLUSIONS = 2
#BUFFER = 0.01 
#SCALE = 0.8
#INCLUSION_SIZE = 0.2

#dist = SizeDistributions.Constant(INCLUSION_SIZE, NUM_INCLUSIONS)
#loc = Locations.RandomLocation(NUM_INCLUSIONS)

#GenerateCircles(NUM_INCLUSIONS, dist, loc)


#NUM_INCLUSIONS = 4
#BUFFER = 0.01 
#SCALE = 0.8
#INCLUSION_SIZE = 0.2

#dist = SizeDistributions.Random(NUM_INCLUSIONS, upper=0.2)
#loc = Locations.RandomLocation(NUM_INCLUSIONS)

#circles = GenerateCircles(NUM_INCLUSIONS, dist, loc)

#for circle in circles:
#    print circle