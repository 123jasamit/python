import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont(None, 30)

# Player
player_size = 50
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
player_health = 100
player_lives = 3
inventory = []

# Areas
areas = ["Forest", "River", "Cave", "Mountains", "Castle",
         "Dragon Lair", "Swamp", "Dark Woods", "Treasure Chamber", "Escape"]
current_area = 0

# Animation
walking_offset = 0
offset_direction = 1

# Enemy movement rate
enemy_update_counter = 0
ENEMY_UPDATE_RATE = 5

# Classes
class Enemy:
    def __init__(self, x, y, size, health, speed, boss=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.health = health
        self.speed = speed
        self.boss = boss

    def move_towards(self, px, py):
        if self.boss:
            if random.random() < 0.02:
                self.rect.x += random.choice([-10,10])
                self.rect.y += random.choice([-10,10])
        else:
            if self.rect.x < px: self.rect.x += self.speed
            elif self.rect.x > px: self.rect.x -= self.speed
            if self.rect.y < py: self.rect.y += self.speed
            elif self.rect.y > py: self.rect.y -= self.speed

class Treasure:
    def __init__(self, x, y, size, name):
        self.rect = pygame.Rect(x, y, size, size)
        self.name = name

# Draw functions
def draw_player(x, y, walking_offset=0):
    pygame.draw.rect(screen, BLUE, (x, y, 40, 50))
    pygame.draw.circle(screen, (0, 100, 255), (x+20, y-10), 10)
    pygame.draw.line(screen, BLUE, (x, y+10), (x-5, y+20+walking_offset), 5)
    pygame.draw.line(screen, BLUE, (x+40, y+10), (x+45, y+20-walking_offset), 5)
    pygame.draw.line(screen, BLUE, (x+10, y+50), (x+10, y+60+walking_offset), 5)
    pygame.draw.line(screen, BLUE, (x+30, y+50), (x+30, y+60-walking_offset), 5)

def draw_sword(x, y):
    pygame.draw.polygon(screen, YELLOW, [(x, y), (x+60, y+10), (x, y+40)])
    pygame.draw.rect(screen, BLACK, (x-5, y+10, 10, 20))

def draw_monster(enemy):
    color = RED if not enemy.boss else PURPLE
    pygame.draw.rect(screen, color, enemy.rect)
    pygame.draw.circle(screen, BLACK, (enemy.rect.x+15, enemy.rect.y+15), 5)
    pygame.draw.circle(screen, BLACK, (enemy.rect.x+enemy.rect.width-15, enemy.rect.y+15), 5)
    pygame.draw.rect(screen, BLACK, (enemy.rect.x+10, enemy.rect.y+enemy.rect.height-10, enemy.rect.width-20, 5))

def draw_text(text, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))

# Create entities
def create_entities(area_level):
    enemies = []
    treasures = []
    num_enemies = min(5 + area_level, 10)
    for _ in range(num_enemies):
        enemies.append(Enemy(random.randint(0, WIDTH-50), random.randint(0, HEIGHT-50), 50, 50+area_level*10, random.randint(1,3)))
    if area_level in [4,5,7,9]:
        enemies.append(Enemy(random.randint(0, WIDTH-60), random.randint(0, HEIGHT-60), 60, 150+area_level*20, 2, boss=True))
    num_treasures = 2 + area_level
    for i in range(num_treasures):
        if area_level == 0 and i == 0:
            treasures.append(Treasure(random.randint(0, WIDTH-40), random.randint(0, HEIGHT-40), 40, "Silver Sword"))
        else:
            treasures.append(Treasure(random.randint(0, WIDTH-40), random.randint(0, HEIGHT-40), 40, random.choice(["Magic Potion","Silver Sword","Gold Coin","Mystic Gem"])))
    return enemies, treasures

enemies, treasures = create_entities(current_area)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        moving = True
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        moving = True
    if keys[pygame.K_UP]:
        player_y -= player_speed
        moving = True
    if keys[pygame.K_DOWN]:
        player_y += player_speed
        moving = True

    # Walking animation
    if moving:
        walking_offset += offset_direction
        if walking_offset > 3 or walking_offset < -3:
            offset_direction *= -1
    else:
        walking_offset = 0

    player_rect = pygame.Rect(player_x, player_y, 40, 50)

    # Use potion
    if keys[pygame.K_h] and "Magic Potion" in inventory:
        player_health += 30
        inventory.remove("Magic Potion")

    # Sword attack
    sword_rect = None
    if keys[pygame.K_SPACE] and "Silver Sword" in inventory:
        draw_sword(player_x+player_size, player_y)
        sword_rect = pygame.Rect(player_x+player_size, player_y, 60, 50)
        for enemy in enemies[:]:
            if sword_rect.colliderect(enemy.rect):
                enemy.health -= 30
                if enemy.health <= 0:
                    enemies.remove(enemy)

    draw_player(player_x, player_y, walking_offset)

    # Move enemies every few frames
    enemy_update_counter += 1
    if enemy_update_counter >= ENEMY_UPDATE_RATE:
        for enemy in enemies:
            enemy.move_towards(player_x, player_y)
        enemy_update_counter = 0

    # Enemies collisions
    for enemy in enemies[:]:
        draw_monster(enemy)
        if player_rect.colliderect(enemy.rect):
            player_health -= 1
            if not sword_rect:
                enemy.health -= 5
            if enemy.health <= 0:
                enemies.remove(enemy)

    # Treasures
    for treasure in treasures[:]:
        pygame.draw.rect(screen, GREEN, treasure.rect)
        if player_rect.colliderect(treasure.rect):
            inventory.append(treasure.name)
            treasures.remove(treasure)

    # Player death
    if player_health <= 0:
        player_lives -= 1
        if player_lives > 0:
            player_health = 1000
            player_x, player_y = WIDTH//2, HEIGHT//2
            enemies, treasures = create_entities(current_area)
        else:
            running = False

    # Area completion
    if not enemies and not treasures:
        if random.random() < 0.4:
            inventory.append("Puzzle Treasure")
        current_area += 1
        if current_area >= len(areas):
            draw_text("Congratulations! You completed the adventure! 🎉", YELLOW, 150, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(5000)
            running = False
        else:
            draw_text(f"Entering {areas[current_area]}...", YELLOW, 250, HEIGHT//2)
            pygame.display.flip()
            pygame.time.delay(2000)
            enemies, treasures = create_entities(current_area)
            player_x, player_y = WIDTH//2, HEIGHT//2

    # HUD
    draw_text(f"Area: {areas[current_area]}", BLACK, 10, 10)
    draw_text(f"Health: {player_health}", BLACK, 10, 40)
    draw_text(f"Lives: {player_lives}", BLACK, 10, 70)
    draw_text(f"Potions (H to use): {inventory.count('Magic Potion')}", BLACK, 10, 100)
    draw_text(f"Sword Equipped (SPACE to swing): {'Silver Sword' in inventory}", BLACK, 10, 130)
    draw_text(f"Inventory: {', '.join(inventory)}", BLACK, 10, 160)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
