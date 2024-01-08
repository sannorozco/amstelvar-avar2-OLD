# menuTitle: extract measurements

import os, glob, json
from variableValues.measurements import FontMeasurements

ufosFolder       = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman/instances/2'
measurementsPath = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman/measurements.json'

ufos = glob.glob(f'{ufosFolder}/*.ufo')

measurements = {}

for ufoPath in ufos:

    fontName = os.path.splitext(os.path.split(ufoPath)[-1])[0]
    styleName = fontName.split('_')[-1]

    f = OpenFont(ufoPath, showInterface=False)

    M = FontMeasurements()
    M.read(measurementsPath)
    M.measure(f)

    measurements[styleName] = M.values

# save blends in JSON format

jsonPath = os.path.join(ufosFolder, 'blends.json')

with open(jsonPath, 'w', encoding='utf-8') as f:
    json.dump(measurements, f, indent=2)
