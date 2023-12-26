# menuTitle: clean-up all sources

'''
- [x] clear colors
- [x] clear libs
- [x] set glyph order (copy from default)
- [x] clear kerning
- [x] clear groups

'''

import os, glob
from hTools3.modules.fontutils import clearMarkColors

familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.getcwd())
sourcesFolder    = os.path.join(baseFolder, 'Parametric-avar2', subFamilyName)
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')
defaultPath      = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_wght400.ufo')

allSources = glob.glob(f'{sourcesFolder}/*.ufo')
# allSources.remove(defaultPath)

clearLibs = [
    'com.fontBureau.measurements',
    'com.fontbureau.variableSpacing.kerning',
    'com.fontbureau.variableSpacing.spacing',
    'com.typemytype.robofont.smartSets',
    'com.typemytype.robofont.smartSets.uniqueKey',
]

defaultFont = OpenFont(defaultPath, showInterface=False)
templateGlyphOrder = defaultFont.templateGlyphOrder
defaultFont.close()

for srcPath in allSources:
    f = OpenFont(srcPath, showInterface=False)
    
    if srcPath != defaultPath:
        # clear mark colors
        clearMarkColors(f)
        # set template glyph order
        f.templateGlyphOrder = templateGlyphOrder
        # clear kerning
        f.kerning.clear()
        # clear groups
        f.groups.clear()

    # clear selected libs
    for k in clearLibs:
        del f.lib[k]
        
    f.save()
    f.close()
