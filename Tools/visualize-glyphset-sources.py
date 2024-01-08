import os, glob
from fontParts.world import OpenFont, RGlyph
from fontTools.pens.transformPen import TransformPointPen
from defcon.objects.component import _defaultTransformation

baseFolder    = os.path.dirname(os.getcwd())
familyName    = 'AmstelvarA2'
subFamily     = ['Roman', 'Italic'][0]
sourcesFolder = os.path.join(baseFolder, 'Source', 'Parametric-avar2', subFamily)
defaultName   = f'{familyName}-{subFamily}_wght400.ufo'
defaultPath   = os.path.join(sourcesFolder, defaultName)
defaultFont   = OpenFont(defaultPath, showInterface=False)
ufoPaths      = glob.glob(f'{sourcesFolder}/*.ufo')
ufoPaths.sort()
ufoPaths.remove(defaultPath)
ufoPaths = [u for u in ufoPaths if 'XTSP' not in u]
# ufoPaths.insert(0, defaultPath)

def drawGlyph(g):
    B = BezierPath()
    g.draw(B)
    drawPath(B)

class DecomposePointPen:

    def __init__(self, glyphSet, outPointPen):
        self._glyphSet = glyphSet
        self._outPointPen = outPointPen
        self.beginPath = outPointPen.beginPath
        self.endPath = outPointPen.endPath
        self.addPoint = outPointPen.addPoint

    def addComponent(self, baseGlyphName, transformation, *args, **kwargs):
        if baseGlyphName in self._glyphSet:
            baseGlyph = self._glyphSet[baseGlyphName]
            if transformation == _defaultTransformation:
                baseGlyph.drawPoints(self)
            else:
                transformPointPen = TransformPointPen(self, transformation)
                baseGlyph.drawPoints(transformPointPen)

ascii = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'.split()

def drawSample(f, s=70, m=100, fallback=True):

    newPage(s*12, s*8 + m)
    blendMode('multiply')

    fill(0,0,1)
    fontSize(24)
    text(f'{f.info.familyName} {f.info.styleName}', (20, 40))

    x, y = 0, height()-s
    _s = 0.02

    _x, _y = x, y
    for gName in ascii:
        if (_x+s) > width():
            _x = x
            _y -= s
        
        stroke(1, 0, 1)
        fill(None)
        rect(_x, _y, s, s)

        if gName in f:
            srcGlyph = f[gName]
            c = 0, 0, 1
        else:
            srcGlyph = defaultFont[gName]
            c = 1, 0, 1

        g = RGlyph()
        pointPen = g.getPointPen()
        decomposePen = DecomposePointPen(f, pointPen)
        srcGlyph.drawPoints(decomposePen)
        g.width = srcGlyph.width

        with savedState():
            translate(_x, _y)
            dx = (s - g.width*_s) / 2

            stroke(None)
            # fill(1, 1, 0)
            # rect(dx, 0, g.width*_s, s)

            translate(dx, s*0.3)
            scale(_s)
            fill(*c)
            drawGlyph(g)

        _x += s


drawSample(defaultFont)

for ufo in ufoPaths:
    f = OpenFont(ufo, showInterface=False)
    print(os.path.split(ufo)[-1])
    drawSample(f)
