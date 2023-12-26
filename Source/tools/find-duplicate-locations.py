from fontTools.designspaceLib import DesignSpaceDocument

designspacePath = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman/AmstelvarA2-Roman.designspace'

D = DesignSpaceDocument()
D.read(designspacePath)

reverseDict = {}

for src in D.sources:
    k = tuple([(k, v) for k, v in src.location.items()])
    if not k in reverseDict:
        reverseDict[k] = []
    reverseDict[k].append(src)

for k, v in reverseDict.items():
    if len(v) > 1:
        for s in v:
            print(s.filename)
        print(k)
