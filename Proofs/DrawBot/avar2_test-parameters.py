# test avar2 variable font in DrawBot

import os
from random import randint 
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from variableValues.measurements import FontMeasurements

folder  = os.path.dirname(os.getcwd())
ttfPath = os.path.join(folder, 'Fonts', 'AmstelvarA2-Roman_avar2.ttf')

newPage('A4Landscape')
font(ttfPath)

fontsize   = 18
lineheight = 1.35

parameters = {
    'opsz': 22,
    'wght': 700,
    'wdth': 120,
}

parameters_all = fontVariations()
for param, value in parameters.items():
    parameters_all[param] = value

p = 20
x = y = p
h = height() - p*2
w = h # width() - p*2

txt = '''OpenType variable fonts are an adaptation of Apple's TrueType GX font variations to OpenType, with integration into key aspects of the OpenType format including OpenType Layout tables and both TrueType and CFF glyph outline formats. It also surpasses TrueType GX by providing better interoperability, both between different fonts, and between variable fonts and font-formatting specifications such as those found in Cascading Style Sheets. The technology allows software to access any design instance for a continuous range of designs defined within the font. When a specific design instance has been selected, the glyph outlines or other data values for that design instance are computed as font data is being processed during text layout and rasterization. The technology uses interpolation and extrapolation mechanisms that have been supported in font-development tools and used by font designers for many years. In that paradigm, the font designer creates a variable design, but then chooses specific instances to generate as static, non-variable fonts that get distributed to customers. With variable fonts, however, the font produced and distributed by the font designer can have built-in variability, and the interpolation mechanisms can now be built into operating systems and Web browsers or other applications, with specific design instances selected at time of use. One of the key benefits of the technology is that it can significantly reduce the combined size of font data whenever multiple styles are in use. On the Web, this may allow a site to use more font styles while at the same time reducing page load times. A further benefit is that it gives access to a continuous range of style variations, which can provide benefits for responsive design.'''

fontVariations(**parameters)

fontSize(fontsize)
lineHeight(fontsize*lineheight)
textBox(txt, (x, y, w, h))

print(parameters_all)

varfont = TTFont(ttfPath)
partial = instancer.instantiateVariableFont(varfont, parameters_all)

partialPath = ttfPath.replace('.ttf', '_current.ttf')
partial.save(partialPath)

measurementsPath = os.path.join(folder, 'Sources', 'Roman', 'measurements.json')

assert os.path.exists(measurementsPath)

f = OpenFont(partialPath, showInterface=False)

measurements = FontMeasurements()
measurements.read(measurementsPath)
measurements.measure(f)

x, y = w+80, w

fontsize   = 12
lineheight = 1.5

fontVariations(resetVariations=True)
font('Menlo')
fontSize(fontsize)

for tag, value in measurements.values.items():
    if tag not in parameters_all:
        continue
    text(f'{tag} {value}', (x, y))
    y -= fontsize * lineheight
