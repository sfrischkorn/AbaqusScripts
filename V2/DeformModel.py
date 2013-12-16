a = mdb.models['Single Inclusion'].rootAssembly

e1 = a.instances['Single Inclusion'].edges

edges1 = e1.getSequenceFromMask(mask=('[#1 ]', ), )

region = a.Set(edges=edges1, name='Set-1')

mdb.models['Single Inclusion'].DisplacementBC(name='BC-1', createStepName='Initial', region=region, u1=UNSET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

mdb.models['Single Inclusion'].StaticStep(name='Step-1', previous='Initial', nlgeom=ON)
mdb.models['Single Inclusion'].steps['Step-1'].setValues(timePeriod=0.01, initialInc=0.01, minInc=1e-07, maxInc=0.01)

mdb.models['Single Inclusion'].boundaryConditions['BC-1'].setValuesInStep(stepName='Step-1', u1=-0.001)

mdb.models['Single Inclusion'].DisplacementBC(name='BC-2', createStepName='Step-1', region=region, u1=UNSET, u2=-0.1, ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
mdb.models['Single Inclusion'].boundaryConditions['BC-2'].setValues(u2=-0.001)

mdb.Job(name='Job-1', model='Single Inclusion', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', multiprocessingMode=DEFAULT, numCpus=1, numGPUs=0)

mdb.jobs['Job-1'].submit(consistencyChecking=OFF)