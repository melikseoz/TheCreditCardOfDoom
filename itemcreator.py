from PIL import Image
import os
items = [
    ('coin', (255, 215, 0)),
    ('gem', (0, 255, 255)),
    ('ring', (255, 105, 180)),
    ('potion', (148, 0, 211)),
    ('scroll', (210, 180, 140)),
    ('shield', (128, 128, 128)),
    ('sword', (192, 192, 192)),
    ('helmet', (105, 105, 105)),
    ('boots', (139, 69, 19)),
    ('amulet', (0, 191, 255)),
]
size = (50, 50)
os.makedirs('images', exist_ok=True)
for name, color in items:
    img = Image.new('RGBA', size, color + (255,))
    img.save(os.path.join('images', f'{name}.png'))
print('done')