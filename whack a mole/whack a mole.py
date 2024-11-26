import pygame
import random
import time
import os

# Pygame initialiseren
pygame.init()

# Scherminstellingen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Whack-a-Mole")

# Kleuren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (171, 80, 0)
DARK_GREEN = (9, 143, 20)

# Afbeeldingen laden
background_img = pygame.image.load("background.JPG")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

mole_img = pygame.image.load("mole.png")
mole_img = pygame.transform.scale(mole_img, (300, 300))

explosion_img = pygame.image.load("explosion.png")
explosion_img = pygame.transform.scale(explosion_img, (300, 300))

button_img = pygame.image.load("button.png")
button_img = pygame.transform.scale(button_img, (350, 150))

# Spelinstellingen
MOLE_POSITIONS = [(80, 210), (500, 210), (890, 210)]
MOLE_APPEAR_TIME = 1.5
MIN_MOLE_TIME = 0.5
MIN_WAIT_TIME = 0.2
MAX_WAIT_TIME = 2.0
score = 0
lives = 3
game_over = False
clock = pygame.time.Clock()
explosion_duration = 0.3
show_explosion = False
explosion_time = 0
mol_visible = True
wait_time = 0
waiting_for_spawn = False

current_mole_position = random.choice(MOLE_POSITIONS)
last_spawn_time = time.time()

font = pygame.font.Font(None, 36)

TIMER_BAR_WIDTH = 200
TIMER_BAR_HEIGHT = 20

HIGH_SCORE_FILE = "highscore.txt"

# Functies voor het beheren van highscore
def load_highscore():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            content = file.read().strip()
            return int(content) if content else 0
    return 0

def save_highscore(new_highscore):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(new_highscore))

# Functie om een mol te spawnen
def spawn_mole():
    global waiting_for_spawn, wait_time, last_spawn_time, mol_visible
    mol_visible = False
    wait_time = random.uniform(MIN_WAIT_TIME, max(MIN_WAIT_TIME, MAX_WAIT_TIME - score * 0.02))
    waiting_for_spawn = True
    last_spawn_time = time.time()

# Functies om statistieken en timer te tonen
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def display_lives():
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

def display_highscore(highscore):
    highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
    screen.blit(highscore_text, (SCREEN_WIDTH // 2 - 70, 10))

def draw_timer_bar(remaining_time, max_time):
    proportion = remaining_time / max_time
    bar_width = int(TIMER_BAR_WIDTH * proportion)
    pygame.draw.rect(screen, RED, (SCREEN_WIDTH - TIMER_BAR_WIDTH - 20, 40, TIMER_BAR_WIDTH, TIMER_BAR_HEIGHT))
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - TIMER_BAR_WIDTH - 20, 40, bar_width, TIMER_BAR_HEIGHT))

# Functies voor gameplay
def calculate_mole_time():
    global MOLE_APPEAR_TIME
    MOLE_APPEAR_TIME = max(MIN_MOLE_TIME, 1.5 - score * 0.02)

def calculate_explosion_duration():
    global explosion_duration
    explosion_duration = max(0.1, 0.3 - score * 0.02)

def display_game_over(final_score, highscore):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 40))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))
    screen.blit(highscore_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 40))
    pygame.display.flip()
    time.sleep(3)

# Functie voor het startscherm
def display_start_screen():
    screen.fill(DARK_GREEN)
    screen.blit(button_img, (465, 285))
    pygame.display.flip()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 465 <= x <= 815 and 285 <= y <= 435:
                    waiting_for_start = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_start = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

# Highscore laden
highscore = load_highscore()

# Startscherm
display_start_screen()

# Spel loop
while not game_over:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            if mol_visible:
                if event.key == pygame.K_a and current_mole_position == MOLE_POSITIONS[0]:
                    score += 10
                    show_explosion = True
                    explosion_time = time.time()
                    spawn_mole()
                elif event.key == pygame.K_s and current_mole_position == MOLE_POSITIONS[1]:
                    score += 10
                    show_explosion = True
                    explosion_time = time.time()
                    spawn_mole()
                elif event.key == pygame.K_d and current_mole_position == MOLE_POSITIONS[2]:
                    score += 10
                    show_explosion = True
                    explosion_time = time.time()
                    spawn_mole()
                else:
                    lives -= 1
                    score -= 20
                    if lives <= 0:
                        game_over = True

    current_time = time.time()
    elapsed_time = current_time - last_spawn_time
    remaining_time = MOLE_APPEAR_TIME - elapsed_time

    calculate_mole_time()
    calculate_explosion_duration()

    if waiting_for_spawn and current_time - last_spawn_time > wait_time:
        current_mole_position = random.choice(MOLE_POSITIONS)
        last_spawn_time = time.time()
        mol_visible = True
        waiting_for_spawn = False

    if mol_visible and remaining_time <= 0:
        spawn_mole()

    if show_explosion and current_time - explosion_time < explosion_duration:
        screen.blit(explosion_img, current_mole_position)
    elif mol_visible:
        screen.blit(mole_img, current_mole_position)

    display_score()
    display_lives()
    display_highscore(highscore)

    if mol_visible:
        draw_timer_bar(remaining_time, MOLE_APPEAR_TIME)

    pygame.display.flip()
    clock.tick(60)

if score > highscore:
    save_highscore(score)

display_game_over(score, highscore)
pygame.quit()
