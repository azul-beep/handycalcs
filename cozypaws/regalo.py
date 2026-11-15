#!/usr/bin/env python3
"""Regalo del newsletter de Cozy Paws: checklist imprimible de cuidado de mascotas (EN y ES).

  python3 cozypaws/regalo.py   -> escribe cozypaws/data/gift/*.pdf (build.py los copia a /gift/)

Se corre una sola vez (o si se cambia el texto). El link va en el mail 1 de bienvenida de MailerLite.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
for n, f in (('Abril', 'AbrilFatface-Regular.ttf'), ('Script', 'Yesteryear-Regular.ttf'), ('Lora', 'Lora.ttf')):
    pdfmetrics.registerFont(TTFont(n, os.path.join(DATA, 'fonts', f)))
CREAM, PLUM, BLUE, GOLD, ROSE, INK = (HexColor(c) for c in ('#F3E9D7', '#3B2433', '#4E7F86', '#C8962E', '#B5525C', '#3a2f2a'))

TXT = {
    'en': dict(
        file='cozy-paws-pet-care-checklist.pdf', title='Pet Care Checklist', sub='A gift from the Cozy Paws Social Club',
        cols=[('Every day', ['Fresh water and clean bowls', 'Meals at the usual times', 'Walk or play time', 'Quick check: eyes, ears, paws', 'Litter box scooped / potty breaks', 'Lots of cuddles']),
              ('Every week', ['Brush the coat', 'Wash food and water bowls well', 'Wash bedding and blankets', 'Check for ticks and fleas', 'Trim treats if weight goes up', 'Try one new trick or toy']),
              ('Every month', ['Flea, tick and heartworm meds', 'Weigh your pet', 'Trim nails', 'Check the collar fit and ID tag', 'Restock food and litter', 'Clean toys, toss broken ones']),
              ('Every year', ['Vet checkup and vaccines', 'Dental check', 'Update microchip contact info', 'Refresh the pet first aid kit', 'New photo for your records', 'Celebrate the gotcha day!'])],
        card='My pet\'s info card', fields=['Name', 'Birthday / gotcha day', 'Breed', 'Microchip #', 'Vet and phone', 'Emergency vet', 'Food and amount', 'Medications', 'Allergies', 'Notes'],
        foot='Cozy Paws · Vintage club gifts for dogs, cats & the people who love them · cozypawsgifts.pages.dev · Free for personal use',
        note='This checklist is a friendly reminder, not veterinary advice. Ask your vet what is right for your pet.'),
    'es': dict(
        file='cozy-paws-checklist-cuidado-mascotas.pdf', title='Checklist de cuidado', sub='Un regalo del Cozy Paws Social Club',
        cols=[('Todos los días', ['Agua fresca y platos limpios', 'Comidas a la hora de siempre', 'Paseo o rato de juego', 'Mirada rápida: ojos, orejas, patas', 'Arenero limpio / salidas al baño', 'Muchos mimos']),
              ('Cada semana', ['Cepillar el pelo', 'Lavar bien los platos', 'Lavar camita y mantas', 'Revisar pulgas y garrapatas', 'Menos premios si sube de peso', 'Probar un truco o juguete nuevo']),
              ('Cada mes', ['Pipeta o pastilla antipulgas', 'Pesar a tu mascota', 'Cortar las uñas', 'Revisar collar y chapita', 'Reponer comida y piedritas', 'Lavar juguetes, tirar los rotos']),
              ('Cada año', ['Control con el veterinario y vacunas', 'Revisión de dientes', 'Actualizar datos del microchip', 'Renovar el botiquín', 'Foto nueva para tus registros', '¡Festejar su cumpleaños!'])],
        card='Ficha de mi mascota', fields=['Nombre', 'Cumpleaños / día de adopción', 'Raza', 'N.º de microchip', 'Veterinario y teléfono', 'Guardia veterinaria', 'Comida y cantidad', 'Medicamentos', 'Alergias', 'Notas'],
        foot='Cozy Paws · Regalos para perros, gatos y la gente que los quiere · cozypawsgifts.pages.dev · Gratis para uso personal',
        note='Este checklist es un recordatorio, no un consejo veterinario. Consultá con tu veterinario qué le conviene a tu mascota.'),
}


def header(c, t, W, H):
    c.setFillColor(CREAM); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(2); c.rect(24, 24, W - 48, H - 48); c.setLineWidth(.6); c.rect(30, 30, W - 60, H - 60)
    logo = os.path.join(DATA, 'brand', 'logo-160.png')
    c.drawImage(logo, W / 2 - 34, H - 118, 68, 68, mask='auto')
    c.setFillColor(PLUM); c.setFont('Script', 22); c.drawCentredString(W / 2, H - 140, t['sub'])


def make(lang):
    t = TXT[lang]
    out = os.path.join(DATA, 'gift'); os.makedirs(out, exist_ok=True)
    c = canvas.Canvas(os.path.join(out, t['file']), pagesize=letter)
    c.setTitle(f"Cozy Paws: {t['title']}"); c.setAuthor('Cozy Paws')
    W, H = letter
    # página 1: checklist
    header(c, t, W, H)
    c.setFillColor(PLUM); c.setFont('Abril', 34); c.drawCentredString(W / 2, H - 182, t['title'])
    colors = [BLUE, ROSE, GOLD, PLUM]
    bw, bh, gap = (W - 60 - 60 - 20) / 2, 238, 20
    for i, (head, items) in enumerate(t['cols']):
        x = 60 + (i % 2) * (bw + gap); y = H - 210 - (i // 2 + 1) * bh - (i // 2) * gap
        c.setFillColor(HexColor('#FAF4E8')); c.setStrokeColor(colors[i]); c.setLineWidth(1.5); c.roundRect(x, y, bw, bh, 10, fill=1)
        c.setFillColor(colors[i]); c.roundRect(x, y + bh - 34, bw, 34, 10, fill=1, stroke=0); c.rect(x, y + bh - 34, bw, 12, fill=1, stroke=0)
        c.setFillColor(HexColor('#FFFFFF')); c.setFont('Abril', 16); c.drawCentredString(x + bw / 2, y + bh - 24, head)
        c.setFillColor(INK); c.setFont('Lora', 11.5)
        for j, it in enumerate(items):
            yy = y + bh - 64 - j * 30
            c.setStrokeColor(colors[i]); c.setLineWidth(1); c.rect(x + 14, yy - 2, 12, 12)
            c.drawString(x + 36, yy, it)
    c.setFillColor(INK); c.setFont('Lora', 8.5); c.drawCentredString(W / 2, 50, t['note']); c.drawCentredString(W / 2, 38, t['foot'])
    c.showPage()
    # página 2: ficha
    header(c, t, W, H)
    c.setFillColor(PLUM); c.setFont('Abril', 34); c.drawCentredString(W / 2, H - 182, t['card'])
    c.setStrokeColor(GOLD); c.setLineWidth(1.5); c.roundRect(W / 2 - 70, H - 345, 140, 140, 12)
    c.setFillColor(GOLD); c.setFont('Script', 18); c.drawCentredString(W / 2, H - 282, 'photo' if lang == 'en' else 'foto')
    y = H - 385
    for f in t['fields']:
        c.setFillColor(PLUM); c.setFont('Abril', 12); c.drawString(70, y, f)
        c.setStrokeColor(BLUE); c.setLineWidth(.8); c.line(70 + pdfmetrics.stringWidth(f, 'Abril', 12) + 8, y - 2, W - 70, y - 2)
        y -= 32
    c.setFillColor(INK); c.setFont('Lora', 8.5); c.drawCentredString(W / 2, 38, t['foot'])
    c.save()


if __name__ == '__main__':
    for lang in TXT:
        make(lang)
    print('ok')
