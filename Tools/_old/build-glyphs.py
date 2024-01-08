import glob
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from hTools3.modules.accents import buildAccentedGlyphs

sourcesFolder         = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman'
glyphConstructionPath = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/AmstelvarA2.glyphConstruction'

glyphNames = ['i', 'j']

# get sources
sources = glob.glob(f'{sourcesFolder}/*.ufo')

# get glyph constructions
with open(glyphConstructionPath, 'r') as f:
    glyphConstructions = f.read()

for srcPath in sources:
    print(f'building glyphs in {srcPath}...')
    font = OpenFont(srcPath, showInterface=False)
    buildAccentedGlyphs(font, glyphNames, glyphConstructions, clear=True, verbose=True, indentLevel=1)
    font.save()
    font.close()
    print()

