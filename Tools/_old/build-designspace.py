import os, glob, shutil
import ufoProcessor
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from variableValues.measurements import FontMeasurements
from defcon import Font
from ufo2ft import compileTTF

'''
Objects to build designspace files for Amstelvar avar2.

0. default
   parametric axes + GRAD
   6 instances for 3 axes extrema

1. default
   parametric axes + GRAD
   blended axes (avar2)

2. default
   parametric axes + GRAD
   6 sources for 3 axes extrema

3. default
   6 sources for 3 axes extrema

* axes extrema:               current values:

  | axis |  min |  max |      |  min |  max |
  |------|------|------|      |------|------|
  | Opsz |    6 |  144 |  ->  |    8 |  144 |
  | Wght |  200 |  700 |  ->  |  100 | 1000 |
  | Wdth |   75 |  125 |  ->  |   50 |  125 |


'''

def permille(value, unitsPerEm):
    return round(value * 1000 / unitsPerEm)


class AmstelvarDesignSpaceBuilder:

    familyName           = 'Amstelvar2'
    subFamilyName        = ['Roman', 'Italic'][1]
    baseFolder           = os.path.dirname(os.getcwd())
    sourcesFolder        = os.path.join(baseFolder,    'TechAlpha', subFamilyName)
    extremaFolder        = os.path.join(sourcesFolder, 'extrema')
    instancesFolder      = os.path.join(sourcesFolder, 'instances')
    measurementsPath     = os.path.join(sourcesFolder, 'measurements.json')
    defaultUFO           = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_wght400.ufo')
    designspacePath      = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}0.designspace')
    blendedAxes          = 'opsz wght wdth'.split()
    parametricAxes       = 'YOPQ YTAS YTDE YTUC YTLC YTFI'.split() # no XOPQ XTRA in italic! # XOPQ XTRA 
    parametricAxesHidden = False

    def __init__(self):
        # collect parametric sources + extrema
        self.sourcesParametric = glob.glob(f'{self.sourcesFolder}/*.ufo')
        self.sourcesExtrema    = glob.glob(f'{self.extremaFolder}/*.ufo')
        # get measurements for default source
        f = OpenFont(self.defaultUFO, showInterface=False)
        self.unitsPerEm = f.info.unitsPerEm
        self.measurementsDefault = FontMeasurements()
        self.measurementsDefault.read(self.measurementsPath)
        self.measurementsDefault.measure(f)
        f.close()

    @property
    def defaultLocation(self):
        L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        L['GRAD'] = 0
        L['XTSP'] = 0
        return L

    def addParametricAxes(self):

        # add grades axis
        a = AxisDescriptor()
        a.name    = 'GRAD'
        a.tag     = 'GRAD'
        a.minimum = -300
        a.maximum = 500
        a.default = 0
        self.designspace.addAxis(a)

        # add spacing axis
        a = AxisDescriptor()
        a.name    = 'XTSP'
        a.tag     = 'XTSP'
        a.minimum = -100
        a.maximum = 100
        a.default = 0
        self.designspace.addAxis(a)

        # add parametric axes
        for name in self.parametricAxes:
            # get min/max values from file names
            values = []
            for ufo in self.sourcesParametric:
                if name in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    values.append(value)
            assert len(values)
            values.sort()
            # create axis
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = values[0]
            a.maximum = values[1]
            a.default = permille(self.measurementsDefault.values[name], self.unitsPerEm)
            a.hidden  = self.parametricAxesHidden
            self.designspace.addAxis(a)

    def addDefaultSource(self):
        # add default source
        src = SourceDescriptor()
        src.path       = self.defaultUFO
        src.familyName = self.familyName
        src.location   = self.defaultLocation.copy()
        self.designspace.addSource(src)

    def addParametricSources(self):

        # add slnt source
        # L = self.defaultLocation.copy()
        # L['slnt'] = -10
        # src = SourceDescriptor()
        # src.path       = os.path.join(self.sourcesFolder, 'RobotoFlex_slnt-10.ufo')
        # src.familyName = self.familyName
        # src.location   = L
        # self.designspace.addSource(src)

        # add GRAD sources
        for gradeValue in [-300, 500]:
            L = self.defaultLocation.copy()
            L['GRAD'] = gradeValue
            src = SourceDescriptor()
            src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_GRAD{gradeValue}.ufo')
            src.familyName = self.familyName
            src.location   = L
            self.designspace.addSource(src)

        # add XTSP sources
        for spacingValue in [-100, 100]:
            L = self.defaultLocation.copy()
            L['XTSP'] = spacingValue
            src = SourceDescriptor()
            src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_XTSP{spacingValue}.ufo')
            src.familyName = self.familyName
            src.location   = L
            self.designspace.addSource(src)

        # add parametric sources
        for name in self.parametricAxes:
            for ufo in self.sourcesParametric:
                if name in ufo:
                    src = SourceDescriptor()
                    src.path       = ufo
                    src.familyName = self.familyName            
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def addInstances(self):
        # prepare to measure fonts
        M = FontMeasurements()
        M.read(self.measurementsPath)

        for blendedAxisName in self.blendedAxes:
            for ufoPath in self.sourcesExtrema:
                if blendedAxisName in ufoPath:
                    # get measurements
                    f = OpenFont(ufoPath, showInterface=False)
                    M.measure(f)

                    # create instance location from default + measurements
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1][4:])
                    valuePermill = permille(value, f.info.unitsPerEm)
                    L[blendedAxisName] = valuePermill
                    for measurementName in self.parametricAxes:
                        valuePermill = permille(int(M.values[measurementName]), f.info.unitsPerEm)
                        L[measurementName] = valuePermill                        

                    # add instance to designspace
                    I = InstanceDescriptor()
                    I.familyName     = self.familyName
                    I.styleName      = f.info.styleName.replace(' ', '')
                    I.name           = f.info.styleName.replace(' ', '')
                    I.designLocation = L
                    I.filename       = os.path.join('instances', f"{self.familyName}-{self.subFamilyName}_{os.path.split(ufoPath)[-1].split('_')[-1]}")
                    self.designspace.addInstance(I)

    def build(self):
        '''Build the designspace object.'''
        self.designspace = DesignSpaceDocument()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        self.addInstances()

    def save(self):
        self.designspace.write(self.designspacePath)

    def buildInstances(self, clear=True, ttf=False):
        if clear:
            instances = glob.glob(f'{self.instancesFolder}/*.ufo')
            for instance in instances:
                shutil.rmtree(instance)
        ufoProcessor.build(self.designspacePath)
        if ttf:
            ufos = glob.glob(f'{self.instancesFolder}/*.ufo')
            print(ufos)
            for ufoPath in ufos:
                ufo = Font(ufoPath)
                ttf = compileTTF(ufo)
                ttfPath = ufoPath.replace('.ufo', '.ttf')
                ttf.save(ttfPath)


class AmstelvarDesignSpaceBuilder1(AmstelvarDesignSpaceBuilder):

    designspacePath = AmstelvarDesignSpaceBuilder.designspacePath.replace('0.designspace', '1.designspace')

    # blended axes data
    axesDefaults = {
        'opsz' : 14,
        'wght' : 400,
        'wdth' : 100,
    }
    axesNames = {
        'opsz' : 'Optical size',
        'wght' : 'Weight',
        'wdth' : 'Width',            
    }

    def addBlendedAxes(self):

        # load measurement definitions
        M = FontMeasurements()
        M.read(self.measurementsPath)

        for tag in self.blendedAxes:
            # get min/max values from file names
            values = []
            for ufo in self.sourcesExtrema:
                if tag in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    values.append(value)
            assert len(values)
            values.sort()

            # create axis
            a = AxisDescriptor()
            a.name    = self.axesNames[tag]
            a.tag     = tag
            a.minimum = values[0]
            a.maximum = values[1]
            a.default = self.axesDefaults[tag]
            self.designspace.addAxis(a)

    def addMappings_avar2(self):

        # load measurement definitions
        M = FontMeasurements()
        M.read(self.measurementsPath)


        for name in self.blendedAxes:
            m = AxisMappingDescriptor()

            for ufo in self.sourcesExtrema:
                if name in ufo:
                    # get input value from file name
                    inputLocation = {}
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    inputLocation[self.axesNames[name]] = value

                    # get output value from measurements
                    f = OpenFont(ufo, showInterface=False)
                    M.measure(f)
                    outputLocation = {}
                    for measurementName in self.parametricAxes:
                        outputLocation[measurementName] = int(M.values[measurementName])

                    m.inputLocation  = inputLocation
                    m.outputLocation = outputLocation

            self.designspace.addAxisMapping(m)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addMappings_avar2()
        self.addDefaultSource()
        self.addParametricSources()


class AmstelvarDesignSpaceBuilder2(AmstelvarDesignSpaceBuilder1):

    designspacePath = AmstelvarDesignSpaceBuilder.designspacePath.replace('0.designspace', '2.designspace')

    @property
    def defaultLocation(self):
        L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        L['Optical size'] = 14
        L['Weight'] = 400
        L['Width'] = 100
        L['GRAD'] = 0
        L['XTSP'] = 0
        return L

    def addBlendedAxes(self):

        # load measurement definitions
        M = FontMeasurements()
        M.read(self.measurementsPath)

        for tag in self.blendedAxes:
            # get min/max values from file names
            values = []
            for ufo in self.sourcesExtrema:
                if tag in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    values.append(value)
            assert len(values)
            values.sort()

            # create axis
            a = AxisDescriptor()
            a.name    = self.axesNames[tag]
            a.tag     = tag 
            a.minimum = values[0]
            a.maximum = values[1]
            a.default = self.axesDefaults[tag]
            self.designspace.addAxis(a)

    def addBlendedSources(self):
        M = FontMeasurements()
        M.read(self.measurementsPath)

        for blendedAxisTag in self.blendedAxes:
            for ufoPath in self.sourcesExtrema:
                if blendedAxisTag in ufoPath:
                    blendedAxisName = self.axesNames[blendedAxisTag]
                    # get measurements
                    f = OpenFont(ufoPath, showInterface=False)
                    M.measure(f)

                    # create instance location from default + measurements
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1][4:])
                    L[blendedAxisName] = value # valuePermill

                    # add instance to designspace
                    src = SourceDescriptor()
                    src.path       = ufoPath
                    src.familyName = self.familyName
                    src.location   = L
                    self.designspace.addSource(src)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addBlendedSources()
        self.addParametricSources()


class AmstelvarDesignSpaceBuilder3(AmstelvarDesignSpaceBuilder2):

    designspacePath = AmstelvarDesignSpaceBuilder.designspacePath.replace('0.designspace', '3.designspace')

    def addParametricAxes(self):

        # add grades axis
        a = AxisDescriptor()
        a.name    = 'GRAD'
        a.tag     = 'GRAD'
        a.minimum = -200
        a.maximum = 150
        a.default = 0
        self.designspace.addAxis(a)

    def addParametricSources(self):

        # add GRAD sources
        for gradeValue in [-300, 500]:
            L = self.defaultLocation.copy()
            L['GRAD'] = gradeValue
            src = SourceDescriptor()
            src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_GRAD{gradeValue}.ufo')
            src.familyName = self.familyName
            src.location   = L
            self.designspace.addSource(src)


# -----
# build
# -----

if __name__ == '__main__':
    
    D = AmstelvarDesignSpaceBuilder()
    D.build()
    D.save()
    D.buildInstances(clear=True, ttf=True)

    D1 = AmstelvarDesignSpaceBuilder1()
    D1.build()
    D1.save()

    D2 = AmstelvarDesignSpaceBuilder2()
    D2.build()
    D2.save()

    D3 = AmstelvarDesignSpaceBuilder3()
    D3.build()
    D3.save()

