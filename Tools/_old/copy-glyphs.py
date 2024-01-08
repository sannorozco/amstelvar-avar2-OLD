import glob
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from hTools3.modules.accents import buildAccentedGlyphs

sourceFont   = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman/AmstelvarA2-Roman_wght400.ufo'
targetFolder = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman'

targetStyles = [
    # 'XOPQ20',
    # 'XOPQ265',
    # 'XTRA234',
    # 'XTRA550',
    # 'XTSP-100',
    # 'XTSP100',
    # 'YOPQ14',
    # 'YOPQ132',
    'YTAS617',
    'YTAS1000',
    'YTDE-138',
    'YTDE-500',
    'YTFI447',
    'YTFI1022',
    # 'YTLC430',
    # 'YTLC581',
    # 'YTUC500',
    # 'YTUC1000',
    # 'GRAD-300',
    # 'GRAD500',
]

glyphNames = ['E', 'Y']

targetFonts = glob.glob(f'{targetFolder}/*.ufo')
targetFonts.remove(sourceFont)

font = OpenFont(sourceFont, showInterface=False)

for dstPath in targetFonts:
    dstFont = OpenFont(dstPath, showInterface=False)

    print(f'copying glyphs to {dstPath}...')
    for glyphName in glyphNames:
        print(f'\tcopying {glyphName}...')
        dstFont.insertGlyph(font[glyphName], name=glyphName)

    dstFont.save()
    dstFont.close()
    print()

