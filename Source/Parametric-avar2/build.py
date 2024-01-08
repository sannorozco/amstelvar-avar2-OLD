import os, glob, shutil, json
import ufoProcessor # upgrade to UFOOperator?
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from variableValues.measurements import FontMeasurements
from defcon import Font
from ufo2ft import compileTTF, compileVariableTTF
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont


def permille(value, unitsPerEm):
    '''Converts a value in font units to a permille value (thousands of em).'''
    return round(value * 1000 / unitsPerEm)

AllFonts
class AmstelvarDesignSpaceBuilder:
    '''
    Simple parametric designspace for use while designing.

    Specialized designspaces for output are created by subclassing this object.

    - parametric axes
    - XTSP

    + builds instances from blends.json file
    + builds variable font

    '''
    familyName      = 'AmstelvarA2'
    subFamilyName   = ['Roman', 'Italic'][0]
    defaultName     = 'wght400'
    parametricAxes  = 'XOPQ XOUC XOLC XOFI XTRA XTUC XTLC XTFI YOPQ YTUC YTLC YTAS YTDE YTFI XSHU YSHU XSVU YSVU XSHL YSHL XSVL YSVL XSHF YSHF XSVF YSVF XTTW YTTL YTOS'.split()
    designspaceName = f'{familyName}-{subFamilyName}.designspace'

    ### move definitions of blended axes to blends.json file?
    blendedAxes     = {
        'wght' : {
            'name'    : 'Weight',
            'default' : 400,
            'min'     : 200,
            'max'     : 800,
        },
        'wdth' : {
            'name'    : 'Width',
            'default' : 100,
            'min'     : 85,
            'max'     : 125,
        },
    }

    def __init__(self):
        # get measurements for default source
        f = OpenFont(self.defaultUFO, showInterface=False)
        self.unitsPerEm = f.info.unitsPerEm
        self.measurementsDefault = FontMeasurements()
        self.measurementsDefault.read(self.measurementsPath)
        self.measurementsDefault.measure(f)
        f.close()

    @property
    def baseFolder(self):
        return os.path.dirname(os.getcwd())

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, 'Parametric-avar2', self.subFamilyName)

    @property
    def instancesFolder(self):
        return os.path.join(self.sourcesFolder, 'instances')

    @property
    def varFontsFolder(self):
        return os.path.join(os.path.dirname(self.baseFolder), 'fonts', 'AsciiAlpha')

    @property
    def varFontPath(self):
        return os.path.join(self.varFontsFolder, self.designspaceName.replace('.designspace', '.ttf'))

    @property
    def measurementsPath(self):
        return os.path.join(self.sourcesFolder, 'measurements.json')

    @property
    def defaultUFO(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{self.defaultName}.ufo')

    @property
    def designspacePath(self):
        return os.path.join(self.sourcesFolder, self.designspaceName)

    @property
    def parametricSources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultLocation(self):
        L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        L['XTSP'] = 0
        return L

    @property
    def blendsPath(self):
        return os.path.join(self.sourcesFolder, 'blends.json')

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
        src.location   = self.defaultLocation
        self.designspace.addSource(src)

    def addParametricSources(self):

        # add spacing sources
        for value in [-100, 100]:
            L = self.defaultLocation.copy()
            L['XTSP'] = value
            src = SourceDescriptor()
            src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_XTSP{value}.ufo')
            src.familyName = self.familyName
            src.styleName  = f'XTSP{value}'
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

    def addInstances(self):

        # load instance data from blends.json file
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blends = json.load(f)

        # add instances to designspace
        for styleName in blends.keys():
            L = self.defaultLocation.copy()
            for axis, value in blends[styleName].items():
                L[axis] = value

            I = InstanceDescriptor()
            I.familyName     = self.familyName
            I.styleName      = styleName
            I.name           = styleName
            I.designLocation = L
            I.filename       = os.path.join('instances', f'{self.familyName}-{self.subFamilyName}_{styleName}.ufo')

            self.designspace.addInstance(I)

    def buildInstances(self, clear=True):

        if clear:
            instances = glob.glob(f'{self.instancesFolder}/*.ufo')
            for instance in instances:
                shutil.rmtree(instance)

        ufoProcessor.build(self.designspacePath)
        ufos = glob.glob(f'{self.instancesFolder}/*.ufo')

        # copy glyph order from default
        f = OpenFont(self.defaultUFO, showInterface=False)
        glyphOrder = f.glyphOrder
        f.close()

        for ufo in ufos:
            f = OpenFont(ufo, showInterface=False)
            f.glyphOrder = glyphOrder
            f.save()
            f.close()

    def addBlendedAxes(self):
        for tag in self.blendedAxes.keys():
            a = AxisDescriptor()
            a.name    = self.blendedAxes[tag]['name']
            a.tag     = tag
            a.minimum = self.blendedAxes[tag]['min']
            a.maximum = self.blendedAxes[tag]['max']
            a.default = self.blendedAxes[tag]['default']
            self.designspace.addAxis(a)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        self.addInstances()

    def save(self):
        if not self.designspace:
            return
        self.designspace.write(self.designspacePath)

    def buildVariableFont(self):

        print(f'generating variable font for {self.designspaceName}...')

        D = DesignSpaceDocument()
        D.read(self.designspacePath)
        print(f'\tloading sources...')
        for src in D.sources:
            src.font = Font(src.path)

        print(f'\tcompiling variable font...')
        f = compileVariableTTF(D, featureWriters=[])
        f.save(self.varFontPath)

        assert os.path.exists(self.varFontPath)

        # subset ascii variable font with pyftsubset
        print('\tsubsetting variable font...')
        font = TTFont(self.varFontPath)
        asciiGlyphs = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'.split()
        subsetter = Subsetter()
        subsetter.populate(glyphs=asciiGlyphs)
        subsetter.subset(font)
        font.save(self.varFontPath)

        print('...done.\n')


class AmstelvarDesignSpaceBuilder_avar1(AmstelvarDesignSpaceBuilder):
    '''
    Designspace for building an avar1 variable font.

    - parametric axes
    - XTSP
    - blended axes: wght wdth
    - wght/wdth extrema defined by instances

    '''

    designspaceName = AmstelvarDesignSpaceBuilder.designspaceName.replace('.designspace', '_avar1.designspace')

    def addBlendedSources(self):
        for tag in self.blendedAxes.keys():
            axisName = self.blendedAxes[tag]['name']
            valueMin = self.blendedAxes[tag]['min']
            valueMax = self.blendedAxes[tag]['max']
            for value in [valueMin, valueMax]:
                ufoPath = os.path.join(self.instancesFolder, f'{self.familyName}-{self.subFamilyName}_{tag}{value}.ufo')
                assert os.path.exists(ufoPath)
                L = self.defaultLocation.copy()
                L[axisName] = value
                src = SourceDescriptor()
                src.path       = ufoPath
                src.familyName = self.familyName
                src.styleName  = f'{tag}{value}'
                src.location   = L
                self.designspace.addSource(src)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        self.addBlendedSources()


class AmstelvarDesignSpaceBuilder_avar2(AmstelvarDesignSpaceBuilder):
    '''
    Designspace for building an avar2 variable font.

    - parametric axes
    - XTSP
    - blended axes: wght wdth
    - wght/wdth extrema defined by avar2 <mappings>

    '''

    designspaceName = AmstelvarDesignSpaceBuilder.designspaceName.replace('.designspace', '_avar2.designspace')

    def addMappings(self):

        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blends = json.load(f)

        for tag in self.blendedAxes:
            for styleName in blends.keys():
                if tag in styleName:
                    m = AxisMappingDescriptor()

                    # get input value from style name
                    inputLocation = {}
                    axisName = self.blendedAxes[tag]['name']
                    value = int(styleName[4:])
                    inputLocation[axisName] = value

                    # get output value from blends.json file
                    outputLocation = {}
                    for axisName in blends[styleName]:
                        outputLocation[axisName] = int(blends[styleName][axisName])

                    m.inputLocation  = inputLocation
                    m.outputLocation = outputLocation

                    self.designspace.addAxisMapping(m)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addMappings()
        self.addDefaultSource()
        self.addParametricSources()


# -----
# build
# -----

if __name__ == '__main__':

    D = AmstelvarDesignSpaceBuilder()
    D.build()
    D.save()
    D.buildInstances()

    D1 = AmstelvarDesignSpaceBuilder_avar1()
    D1.build()
    D1.save()
    D1.buildVariableFont()

    D2 = AmstelvarDesignSpaceBuilder_avar2()
    D2.build()
    D2.save()
    D2.buildVariableFont()
