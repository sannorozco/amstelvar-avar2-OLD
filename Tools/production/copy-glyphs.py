# menuTitle: copy default glyphs to other sources

import os, glob

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
sourceName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePath    = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{sourceName}.ufo')

assert os.path.exists(sourcePath)

glyphNames = 'gravecomb acutecomb circumflexcomb tildecomb macroncomb brevecomb dotaccentcomb dieresiscomb hookabovecomb ringcomb hungarumlautcomb caroncomb breveinvertedcomb dblgravecomb horncomb dotbelowcomb dieresisbelowcomb commaaccentcomb cedillacomb ogonekcomb brevebelowcomb macronbelowcomb commaaccentturnedcomb gravecomb.case acutecomb.case dieresiscomb.case macroncomb.case cedillacomb.case circumflexcomb.case caroncomb.case brevecomb.case dotaccentcomb.case ringcomb.case ogonekcomb.case tildecomb.case hungarumlautcomb.case hookabovecomb.case breveinvertedcomb.case dblgravecomb.case horncomb.case dotbelowcomb.case dieresisbelowcomb.case commaaccentcomb.case brevebelowcomb.case macronbelowcomb.case caroncomb.alt tonoscomb tonoscomb.case dieresistonoscomb breve.cyrcomb.case breve.cyrcomb yi-dieresiscomb'.split()

dstFonts = [] # 'XUCS114 XUCS259'.split()
    
preflight = False

sourceFont = OpenFont(sourcePath, showInterface=False)
ufoPaths = glob.glob(f'{sourcesFolder}/*.ufo')

for ufoPath in ufoPaths:
    if ufoPath == sourcePath:
        continue

    name = os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1]
    if name in dstFonts or not dstFonts:

        dstFont = OpenFont(ufoPath, showInterface=False)

        print(f'copying glyphs to {ufoPath}...')
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
