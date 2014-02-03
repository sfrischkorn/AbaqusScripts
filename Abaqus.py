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


def GenerateModel(inclusions, matrix_material, matrix_mesh_control):
    #Define constants
    modelName = 'Single Inclusion'
    partName = 'Part-1'
    matrix_material_name = 'Matrix'
    matrix_section_name = 'Matrix'
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


    #assign matrix materials
    for command in matrix_material.generate_material_commands("myModel", matrix_section_name):
        exec(command)


    p = myModel.parts[partName]
    f = p.faces


    i = 0
    for inclusion, inclusion_mesh_control in inclusions:
        commands = inclusion.GenerateSketch()

        for command in commands:
            exec(command)

        inclusionFaces = f.findAt(((inclusion.centre[0], inclusion.centre[1], 0.0), ))
        p.PartitionFaceBySketch(faces=inclusionFaces, sketch=s)

        del s
        i += 1

        setname = inclusionSetName + str(i)
        sectionname = inclusionSectionName + str(i)
        for material_command in inclusion.material.generate_material_commands("myModel", sectionname):
            exec(material_command)

        #this is already assigned above, but it loses the definition and needs to be assigned again
        inclusionFaces = f.findAt(((inclusion.centre[0], inclusion.centre[1], 0.0), ))
        inclusionRegion = p.Set(faces=inclusionFaces, name=setname)
        p.SectionAssignment(region=inclusionRegion, sectionName=sectionname, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
        #p.setMeshControls(regions=inclusionFaces, elemShape=inclusion_mesh_control.elem_shape, technique=inclusion_mesh_control.technique, algorithm=inclusion_mesh_control.algorithm, minTransition=inclusion_mesh_control.min_transition, sizeGrowth=inclusion_mesh_control.size_growth, allowMapped=inclusion_mesh_control.allow_mapped)
        cmd = inclusion_mesh_control.GenerateCommand('inclusionFaces')
        exec(cmd)


    #Create sets and sections
    matrixFaces = f.findAt(((0.001, 0.001, 0.0), )) # TODO: find a way to find a spot that isn't taken with inclusions
    matrixRegion = p.Set(faces=matrixFaces, name=setName)
    p.SectionAssignment(region=matrixRegion, sectionName=matrix_section_name, offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
    #p.setMeshControls(regions=matrixFaces, elemShape=matrix_mesh_control.elem_shape, technique=matrix_mesh_control.technique, algorithm=matrix_mesh_control.algorithm, minTransition=matrix_mesh_control.min_transition, sizeGrowth=matrix_mesh_control.size_growth, allowMapped=matrix_mesh_control.allow_mapped)
    cmd = matrix_mesh_control.GenerateCommand('matrixFaces')
    exec(cmd)


    #Create the assembly
    assembly = myModel.rootAssembly
    assembly.DatumCsysByDefault(CARTESIAN)
    assembly.Instance(name=assemblyName, part=p, dependent=ON)

    #Mesh the part
    p.seedPart(size=0.01)
    p.generateMesh()