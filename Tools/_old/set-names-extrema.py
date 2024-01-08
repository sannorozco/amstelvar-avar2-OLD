import os, glob, shutil

subFamilyName = ['Roman', 'Italic'][0]
baseFolder    = os.path.dirname(os.getcwd())
sourcesFolder = os.path.join(baseFolder, 'sources', subFamilyName)
extremaFolder = os.path.join(sourcesFolder, 'extrema')

allUFOs = glob.glob(f'{extremaFolder}/*.ufo')

for ufo in allUFOs:
    styleName = os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1]
    f = OpenFont(ufo, showInterface=False)
    f.info.styleName = styleName
    f.save()
    f.close()
