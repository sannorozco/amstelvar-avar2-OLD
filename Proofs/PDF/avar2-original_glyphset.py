import os, json

proofsFolder  = os.path.dirname(os.getcwd())
baseFolder    = os.path.dirname(proofsFolder)
fontsFolder   = os.path.join(baseFolder, 'Fonts')

font1_name    = 'Amstelvar'
font1_Roman   = os.path.join(proofsFolder, 'Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf')
font1_Italic  = os.path.join(proofsFolder, 'Amstelvar-Italic[GRAD,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf')
font1_label   = 'AmstelvarA2 avar2'

font2_name    = 'AmstelvarA2'
font2_Roman   = os.path.join(fontsFolder, 'AmstelvarA2-Roman_avar2.ttf')
font2_Italic  = os.path.join(fontsFolder, 'AmstelvarA2-Italic_avar2.ttf')
font2_label   = 'Amstelvar original'

ASCII  = '''\
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
0123456789 .,:;!? @#$%&*
{|}[\](/)_<=>+~- '"^`
'''

p  = 18
fs = 28

savePDF = False

subFamilyName = ['Roman', 'Italic'][0]

font1 = font1_Roman if subFamilyName == 'Roman' else font1_Italic
font2 = font2_Roman if subFamilyName == 'Roman' else font2_Italic

proofName = f'avar2-original_ASCII_glyphset_{subFamilyName}.pdf'
pdfPath = os.path.join(os.getcwd(), proofName)

for opsz in [8, 14, 144]:
    for wdth in [50, 100, 150]:
        for wght in range(100, 1001, 100):
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

            # HACK TO MAKE AVAR2 FONT WORK
            font(font2)
            _variations = fontVariations()
            for k, v in variations.items():
                _variations[k] = v

            T2 = FormattedString()
            T2.font(font2)
            T2.fontSize(fs)
            T2.lineHeight(fs*1.3)
            T2.fontVariations(**_variations)
            T2.append(ASCII, align='center')

            textBox(T2, (p, p, W, H*2))
            textBox(T1, (p, p, W, H))

            with savedState():
                txt1 = f'{font1_name} {subFamilyName}'
                txt2 = f'{font2_name} {subFamilyName}'
                font('Menlo')
                fontSize(9)
                fill(1, 0, 0)
                with savedState():
                    translate(p, height()*0.5)
                    rotate(90)
                    text(txt1, (-H*0.5, 0), align='left')
                    text(txt2, (H*0.5, 0), align='left')

                text(f'opsz{opsz} wght{wght} wdth{wdth}', (W/2, p), align='center')

if savePDF:
    saveImage(pdfPath)

