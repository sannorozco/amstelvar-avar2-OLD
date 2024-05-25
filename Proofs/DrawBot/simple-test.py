import os

style = ['Roman', 'Italic'][0]
baseFolder = os.path.dirname(os.path.dirname(os.getcwd()))
fontPath = os.path.join(baseFolder, 'Fonts', f'AmstelvarA2-{style}_avar2.ttf')

ASCII  = '''\
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789 .,:;!? @#$%&*
{|}[\](/)_<=>+~- '"^`
'''

newPage('A4Landscape')
font(fontPath)
fontSize(36)
fontVariations(**fontVariations()) # WEIRD!!
text(ASCII, (width()/2, height()*0.6), align='center')
