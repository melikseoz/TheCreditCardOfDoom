# TheCreditCardOfDoom

A simple inventory selling game built with Pygame.

## How to run

1. Install dependencies:
   ```bash
   pip install pygame
   ```
2. Run the game:
   ```bash
   python game.py
   ```

Every few seconds a random item appears in your inventory. Drag items to the red sell box to earn money. Your total earnings are displayed at the top left.

### Item images

Item images are loaded from the `images/` folder. Each image is scaled to `50x50` pixels to match the item slot size. To customize an item, add a PNG named after the item (e.g. `coin.png`, `gem.png`) into this folder. If an image is missing the game falls back to the colored rectangle.