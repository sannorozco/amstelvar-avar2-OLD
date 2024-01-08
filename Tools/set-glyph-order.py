# menuTitle: set glyph order

import os, glob
from hTools3.modules.encoding import setGlyphOrder

baseFolder     = os.path.dirname(os.getcwd())
familyName     = 'AmstelvarA2'
subFamily      = ['Roman', 'Italic'][0]
sourcesFolder  = os.path.join(baseFolder, 'Source', 'Parametric-avar2', subFamily)
encodingPath   = os.path.join(baseFolder, 'Source', 'Parametric-avar2', 'AmstelvarA2.enc')
defaultName    = f'{familyName}-{subFamily}_wght400.ufo'
excludeDefault = True
ufoPaths       = glob.glob(f'{sourcesFolder}/*.ufo')

if excludeDefault:
    ufoPaths.remove(os.path.join(sourcesFolder, defaultName))

def fontName(ufoPath):
    return os.path.split(ufoPath)[-1]

def batchSetGlyphOrder(ufoPaths):
    print('setting glyph order in all sources…')
    for ufoPath in ufoPaths:
        font = OpenFont(ufoPath, showInterface=False)
        print(f'\tsetting glyph order in {fontName(ufoPath)}…')
        setGlyphOrder(font, encodingPath, verbose=False, createTemplates=True, createGlyphs=False)
        font.save()
    print('…done.\n')

def batchClearTemplateGlyphs(ufoPaths):
    print('deleting template glyphs in all sources…')
    for ufoPath in ufoPaths:
        font = OpenFont(ufoPath, showInterface=False)
        print(f'\tdeleting template glyphs in {fontName(ufoPath)}…')
        glyphOrder = [g for g in font.templateGlyphOrder if g in font]
        font.glyphOrder = glyphOrder
        font.save()
    print('…done.\n')

# batchSetGlyphOrder(ufoPaths)
batchClearTemplateGlyphs(ufoPaths)
