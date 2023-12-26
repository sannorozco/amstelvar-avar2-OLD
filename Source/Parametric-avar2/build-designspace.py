import os, glob, shutil
import ufoProcessor
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from variableValues.measurements import FontMeasurements
from defcon import Font
from ufo2ft import compileTTF

def permille(value, unitsPerEm):
    return round(value * 1000 / unitsPerEm)

class AmstelvarDesignSpaceBuilder:

    familyName       = 'AmstelvarA2'
    subFamilyName    = ['Roman', 'Italic'][0]
    baseFolder       = os.path.dirname(os.getcwd())
    sourcesFolder    = os.path.join(baseFolder,    'Parametric-avar2', subFamilyName) # 'TechAlpha'
    measurementsPath = os.path.join(sourcesFolder, 'measurements.json')
    defaultName      = 'wght400'
    defaultUFO       = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{defaultName}.ufo')
    designspacePath  = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}.designspace')
    parametricAxes   = 'XOPQ XTRA YOPQ YTUC YTLC YTAS YTDE YTFI XSHA YSHA XSVA YSVA XTTW YTTL YTOS'.split() # XOUC XOLC XOFI XTUC XTLC XTFI XSHU XSHL XSHF  YSHU YSHL YSHF  XSVU XSVL XSVF YSVU YSVL YSVF 
    minValue         = -100
    maxValue         = 100

    def __init__(self):
        # get measurements for default source
        f = OpenFont(self.defaultUFO, showInterface=False)
        self.unitsPerEm = f.info.unitsPerEm
        self.measurementsDefault = FontMeasurements()
        self.measurementsDefault.read(self.measurementsPath)
        self.measurementsDefault.measure(f)
        f.close()

    @property
    def parametricSources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultLocation(self):
        L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        L['XTSP'] = 0
        return L

    def addParametricAxes(self):

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
            for ufo in self.parametricSources:
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
            self.designspace.addAxis(a)

    def addDefaultSource(self):
        src = SourceDescriptor()
        src.path       = self.defaultUFO
        src.familyName = self.familyName
        src.styleName  = self.defaultName
        src.location   = self.defaultLocation.copy()
        self.designspace.addSource(src)

    def addParametricSources(self):

        # add XTSP sources
        for spacingValue in [-100, 100]:
            L = self.defaultLocation.copy()
            L['XTSP'] = spacingValue
            src = SourceDescriptor()
            src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_XTSP{spacingValue}.ufo')
            src.familyName = self.familyName
            src.styleName  = f'XTSP{spacingValue}'
            src.location   = L
            self.designspace.addSource(src)

        # add parametric sources
        for name in self.parametricAxes:
            for ufo in self.parametricSources:
                if name in ufo:
                    src = SourceDescriptor()
                    src.path       = ufo
                    src.familyName = self.familyName
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    src.styleName  = f'{name}{value}'
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()

    def save(self):
        if not self.designspace:
            return
        self.designspace.write(self.designspacePath)


# -----
# build
# -----

if __name__ == '__main__':

    D = AmstelvarDesignSpaceBuilder()
    D.build()
    D.save()
