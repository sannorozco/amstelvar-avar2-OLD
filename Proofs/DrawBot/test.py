import os, json

fontPath = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Fonts/AmstelvarA2-Roman_avar2.ttf'

ASCII  = '''\
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789 .,:;!? @#$%&*
{|}[\](/)_<=>+~- '"^`
'''

print(listFontVariations(fontPath))

p = 18
fs = 36

newPage('A4Landscape')

W = width()-p*2
H = (height()-p*3) / 2

font(fontPath)
#lineHeight(fs*1.3)
fontSize(fs)
fontVariations(opsz=8, wght=400)
text(ASCII, (W/2, H*1.3), align='center')
