import os, json

subFamilyName = ['Roman', 'Italic'][0]

baseFolder    = os.path.dirname(os.getcwd())
fontsFolder   = os.path.join(baseFolder, 'Fonts')

font1_name    = 'Amstelvar'
font1_Roman   = 'Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf'
font1_Italic  = 'Amstelvar-Italic[GRAD,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf'
font1_label   = 'AmstelvarA2 avar2'

font2_name    = 'AmstelvarA2'
font2_Roman   = os.path.join(fontsFolder, 'AmstelvarA2-Roman_avar2.ttf')
font2_Italic  = os.path.join(fontsFolder, 'AmstelvarA2-Italic_avar2.ttf')
font2_label   = 'Amstelvar original'

font1 = font1_Roman if subFamilyName == 'Roman' else font1_Italic
font2 = font2_Roman if subFamilyName == 'Roman' else font2_Italic

proof_file    = 'avar2-original_compare-DB.pdf'

ASCII  = '''\
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789 .,:;!? @#$%&*
{|}[\](/)_<=>+~- '"^`
'''

p = 18
fs = 29


# for wdth in [100, 50, 150]:
wdth = 100
for opsz in [14, 8, 144]:
    for wght in range(100, 1000, 100):
        variations = {
            'opsz' : opsz,
            'wght' : wght,
            'wdth' : wdth,
        }
        newPage('A4Landscape')

        W = width()-p*2
        H = (height()-p*3) / 2

        T1 = FormattedString()
        T1.font(font1)
        T1.fontSize(fs)
        T1.lineHeight(fs*1.3)
        T1.fontVariations(**variations)
        T1.append(ASCII, align='center')

        T2 = FormattedString()
        T2.font(font2)
        T2.fontSize(fs)
        T2.lineHeight(fs*1.3)
        T2.fontVariations(**variations)
        T2.append(ASCII, align='center')

        textBox(T2, (p, p, W, H*2))
        textBox(T1, (p, p, W, H))

        with savedState():
            font('Menlo-Bold')
            fill(1, 0, 0)
            fontSize(11)
            with savedState():
                translate(p, height()*0.5)
                rotate(90)
                text(f'{font1_name} {subFamilyName}', (-H/2, 0), align='left')
                text(f'{font2_name} {subFamilyName}', (H/2, 0), align='left')

            text(f'opsz{opsz} wght{wght} wdth{wdth}', (W/2, p), align='center')

