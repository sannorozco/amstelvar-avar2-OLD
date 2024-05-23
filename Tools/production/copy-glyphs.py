# menuTitle: copy default glyphs to other sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][0]
sourceName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePath    = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{sourceName}.ufo')

assert os.path.exists(sourcePath)

glyphNames = 'l o u x Ustraightstroke Hastroke-cy I O T X Zhe Ka Che Sha Shcha Yu Zhedescender Kadescender Endescender Tedescender-cy Hadescender Chedescender-cy Obarcyr zhe ka en te che sha shcha yeru soft yu zhedescender kadescender endescender tedescender-cy hadescender chedescender-cy obarcyr hastroke-cy tse.bgr sha.bgr shcha.bgr Yumacron yumacron Yu-dash.case yu.bgr-stroke'.split() # H

dstFonts = 'XUCS32 XUCS205'.split()
    
preflight = False

sourceFont = OpenFont(sourcePath, showInterface=False)
ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

for ufoPath in ufoPaths:
    if ufoPath == sourcePath:
        continue

    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:

        dstFont = OpenFont(ufoPath, showInterface=False)

        print(f'copying glyphs to {os.path.split(ufoPath)[-1]}...')
        for glyphName in glyphNames:
            if glyphName not in sourceFont:
                print(f'\tERROR: {glyphName} not in source font')
                continue
            print(f'\tcopying {glyphName}...')
            if not preflight:
                dstFont.insertGlyph(sourceFont[glyphName], name=glyphName)

        if not preflight:
            print(f'\tsaving font...')
            dstFont.save()

        dstFont.close()
        print()
