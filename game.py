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

# Define sell area
SELL_AREA = pygame.Rect(WIDTH - 160, HEIGHT - 160, 150, 150)

# Define 10 unique items
ITEMS = [
    {'name': 'Coin', 'color': (255, 215, 0), 'value': 10},
    {'name': 'Gem', 'color': (0, 255, 255), 'value': 50},
    {'name': 'Ring', 'color': (255, 105, 180), 'value': 30},
    {'name': 'Potion', 'color': (148, 0, 211), 'value': 40},
    {'name': 'Scroll', 'color': (210, 180, 140), 'value': 20},
    {'name': 'Shield', 'color': (128, 128, 128), 'value': 60},
    {'name': 'Sword', 'color': (192, 192, 192), 'value': 80},
    {'name': 'Helmet', 'color': (105, 105, 105), 'value': 35},
    {'name': 'Boots', 'color': (139, 69, 19), 'value': 25},
    {'name': 'Amulet', 'color': (0, 191, 255), 'value': 45},
]

# Inventory slots positions
INVENTORY_SLOTS = [
    pygame.Rect(10 + i * (ITEM_SIZE + 10), HEIGHT - ITEM_SIZE - 10, ITEM_SIZE, ITEM_SIZE)
    for i in range(INVENTORY_SIZE)
]
INVENTORY = [None] * INVENTORY_SIZE

def spawn_item():
    """Add a random item to the first available inventory slot."""
    for i in range(INVENTORY_SIZE):
        if INVENTORY[i] is None:
            item = random.choice(ITEMS).copy()
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
        pygame.draw.rect(SCREEN, (150, 0, 0), SELL_AREA, 2)
        for slot in INVENTORY_SLOTS:
            pygame.draw.rect(SCREEN, (200, 200, 200), slot, 2)
        for item in INVENTORY:
            if item:
                pygame.draw.rect(SCREEN, item['color'], item['rect'])

        total_text = font.render(f'Total: ${total_money}', True, (255, 255, 255))
        SCREEN.blit(total_text, (10, 10))

        pygame.display.flip()
        CLOCK.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
