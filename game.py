import os
import random
import pygame

# Allow headless execution for automated checks
if os.environ.get('PYGAME_HEADLESS'):
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Inventory Seller')
CLOCK = pygame.time.Clock()

ITEM_SPAWN_INTERVAL = 3000  # milliseconds
INVENTORY_SIZE = 5
ITEM_SIZE = 50

# Asset handling
ASSET_DIR = os.path.join(os.path.dirname(__file__), "images")


def load_item_image(filename: str):
    """Load and scale an item image if it exists."""
    path = os.path.join(ASSET_DIR, filename)
    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (ITEM_SIZE, ITEM_SIZE))
    return None

# Define interaction areas
SELL_AREA = pygame.Rect(WIDTH - 160, HEIGHT - 160, 150, 150)
TRASH_AREA = pygame.Rect(WIDTH - 160, 10, 150, 150)

# Define 10 unique items
ITEMS = [
    {
        'name': 'Coin',
        'color': (255, 215, 0),
        'value': 10,
        'image': load_item_image('coin.png'),
    },
    {
        'name': 'Gem',
        'color': (0, 255, 255),
        'value': 150,
        'image': load_item_image('gem.png'),
    },
    {
        'name': 'Sword Cutter',
        'color': (255, 105, 180),
        'value': 150,
        'image': load_item_image('swordcutter.png'),
    },
    {
        'name': 'Portal Potion',
        'color': (148, 0, 211),
        'value': 150,
        'image': load_item_image('portalpotion.png'),
    },
    {
        'name': 'Scroll',
        'color': (210, 180, 140),
        'value': 20,
        'image': load_item_image('scroll.png'),
    },
    {
        'name': 'Shield',
        'color': (128, 128, 128),
        'value': 60,
        'image': load_item_image('shield.png'),
    },
    {
        'name': 'Sword',
        'color': (192, 192, 192),
        'value': 80,
        'image': load_item_image('sword.png'),
    },
    {
        'name': 'Helmet',
        'color': (105, 105, 105),
        'value': 35,
        'image': load_item_image('helmet.png'),
    },
    {
        'name': 'Boots',
        'color': (139, 69, 19),
        'value': 25,
        'image': load_item_image('boots.png'),
    },
    {
        'name': 'Amulet',
        'color': (0, 191, 255),
        'value': 45,
        'image': load_item_image('amulet.png'),
    },
]

# Inventory slots positions
INVENTORY_SLOTS = [
    pygame.Rect(10 + i * (ITEM_SIZE + 10), HEIGHT - ITEM_SIZE - 10, ITEM_SIZE, ITEM_SIZE)
    for i in range(INVENTORY_SIZE)
]
INVENTORY = [None] * INVENTORY_SIZE

def spawn_item():
    """Add a random item (or trash) to the first available inventory slot."""
    for i in range(INVENTORY_SIZE):
        if INVENTORY[i] is None:
            if random.random() < 0.2:
                item = {
                    'name': 'Trash',
                    'is_trash': True,
                    'value': -80,
                    'rect': INVENTORY_SLOTS[i].copy(),
                }
            else:
                item = random.choice(ITEMS).copy()
                item['is_trash'] = False
                item['rect'] = INVENTORY_SLOTS[i].copy()
            INVENTORY[i] = item
            return


def main():
    running = True
    total_money = 0
    dragged_index = None
    drag_offset = (0, 0)
    last_spawn = pygame.time.get_ticks()

    font = pygame.font.Font(None, 36)
    info_font = pygame.font.Font(None, 24)
    sold_items = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, item in enumerate(INVENTORY):
                    if item and item['rect'].collidepoint(event.pos):
                        dragged_index = idx
                        drag_offset = (item['rect'].x - event.pos[0], item['rect'].y - event.pos[1])
                        break
            elif event.type == pygame.MOUSEBUTTONUP and dragged_index is not None:
                item = INVENTORY[dragged_index]
                if SELL_AREA.colliderect(item['rect']):
                    total_money += item['value']
                    sold_items.append((item['name'], item['value']))
                    if len(sold_items) > 5:
                        sold_items.pop(0)
                    INVENTORY[dragged_index] = None
                elif TRASH_AREA.colliderect(item['rect']):
                    INVENTORY[dragged_index] = None
                else:
                    item['rect'].topleft = INVENTORY_SLOTS[dragged_index].topleft
                dragged_index = None

        # Update dragged item position
        if dragged_index is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            item = INVENTORY[dragged_index]
            item['rect'].topleft = (mouse_x + drag_offset[0], mouse_y + drag_offset[1])

        # Spawn items periodically
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn > ITEM_SPAWN_INTERVAL:
            spawn_item()
            last_spawn = current_time

        # Drawing
        SCREEN.fill((30, 30, 30))
        pygame.draw.rect(SCREEN, (0, 150, 0), SELL_AREA, 2)
        pygame.draw.rect(SCREEN, (150, 0, 0), TRASH_AREA, 2)
        sell_text = info_font.render('Sell', True, (0, 150, 0))
        sell_rect = sell_text.get_rect(center=SELL_AREA.center)
        SCREEN.blit(sell_text, sell_rect)
        trash_text = info_font.render('Trash', True, (150, 0, 0))
        trash_rect = trash_text.get_rect(center=TRASH_AREA.center)
        SCREEN.blit(trash_text, trash_rect)
        for slot in INVENTORY_SLOTS:
            pygame.draw.rect(SCREEN, (200, 200, 200), slot, 2)
        mouse_pos = pygame.mouse.get_pos()
        tooltip = None
        tooltip_rect = None
        for item in INVENTORY:
            if item:
                if item.get('is_trash'):
                    pygame.draw.line(
                        SCREEN,
                        (255, 0, 0),
                        item['rect'].topleft,
                        item['rect'].bottomright,
                        3,
                    )
                    pygame.draw.line(
                        SCREEN,
                        (255, 0, 0),
                        item['rect'].topright,
                        item['rect'].bottomleft,
                        3,
                    )
                elif item.get('image'):
                    SCREEN.blit(item['image'], item['rect'])
                else:
                    pygame.draw.rect(SCREEN, item['color'], item['rect'])
                if item['rect'].collidepoint(mouse_pos) and not item.get('is_trash'):
                    tooltip = info_font.render(
                        f"{item['name']} - ${item['value']}", True, (255, 255, 255)
                    )
                    tooltip_rect = tooltip.get_rect()
                    tooltip_rect.topleft = (
                        mouse_pos[0] + 10,
                        mouse_pos[1] - tooltip_rect.height - 10,
                    )

        total_text = font.render(f'Total: ${total_money}', True, (255, 255, 255))
        SCREEN.blit(total_text, (10, 10))

        y_offset = 50
        for name, value in reversed(sold_items):
            sold_text = info_font.render(f"{name} - ${value}", True, (255, 255, 255))
            SCREEN.blit(sold_text, (10, y_offset))
            y_offset += 20

        if tooltip:
            background = tooltip_rect.inflate(4, 4)
            pygame.draw.rect(SCREEN, (0, 0, 0), background)
            SCREEN.blit(tooltip, tooltip_rect)

        pygame.display.flip()
        CLOCK.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
