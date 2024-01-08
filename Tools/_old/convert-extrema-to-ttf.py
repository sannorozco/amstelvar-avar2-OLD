import os, glob, shutil
from defcon import Font
from ufo2ft import compileTTF

familyName      = 'Amstelvar'
subFamilyName   = ['Roman', 'Italic'][0]
baseFolder      = os.path.dirname(os.getcwd())
sourcesFolder   = os.path.join(baseFolder, 'sources', subFamilyName)
extremaFolder   = os.path.join(sourcesFolder, 'extrema')

assert os.path.exists(extremaFolder)

ufos = glob.glob(f'{extremaFolder}/*.ufo')

for ufoPath in ufos:
    ufo = Font(ufoPath)
    ttf = compileTTF(ufo)
    ttfPath = ufoPath.replace('.ufo', '.ttf')
    ttf.save(ttfPath)
