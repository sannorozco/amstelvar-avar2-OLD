from fontTools.designspaceLib import DesignSpaceDocument #, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor

designspacePath = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman/AmstelvarA2-Roman.designspace'

doc = DesignSpaceDocument()
doc.read(designspacePath)

axes = { axis.tag: axis for axis in doc.axes }

for instance in doc.instances:
    print(instance.name)
    for axisName, value in instance.designLocation.items():
        axis = axes[axisName]
        if not axis.minimum <= value <= axis.maximum:
            print(axisName, value, axis.minimum, axis.maximum)
    print()
