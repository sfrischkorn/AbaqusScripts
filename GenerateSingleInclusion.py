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

# Create a partition for the inclusion
t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0.5, 0.5, 0.0))
s = myModel.ConstrainedSketch(name='__profile__', sheetSize=20.0, transform=t)
s.setPrimaryObject(option=SUPERIMPOSE)
s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.25, 0.25))

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

matrixFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
matrixRegion = p.Set(faces=matrixFaces, name=inclusionSetName)
p.SectionAssignment(region=matrixRegion, sectionName=inclusionSectionName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

inclusionFaces = f.getSequenceFromMask(mask=('[#2 ]', ), )
inclusionRegion = p.Set(faces=inclusionFaces, name=setName)
p.SectionAssignment(region=inclusionRegion, sectionName=mySectionName, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)


#Create the assembly
assembly = myModel.rootAssembly
assembly.DatumCsysByDefault(CARTESIAN)
assembly.Instance(name=assemblyName, part=p, dependent=ON)

regionsToMesh = matrixRegion, inclusionRegion,
#create the mesh
p.setMeshControls(regions=inclusionFaces, elemShape=TRI)
p.seedPart(size=0.1)
p.generateMesh()

